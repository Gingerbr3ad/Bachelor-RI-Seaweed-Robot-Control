import copy
import numpy as np

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from rclpy.duration import Duration

import tf2_ros
import tf2_geometry_msgs  # needed for PoseStamped TF support

from geometry_msgs.msg import PoseStamped
from std_srvs.srv import SetBool

from ri_seaweed_interfaces.srv import GetObjects
from ri_seaweed_interfaces.action import MoveToPose

from scipy.spatial.transform import Rotation


class AutoPickUpExample(Node):
    def __init__(self):
        super().__init__('auto_pick_up_example')

        self.target_frame = 'fr3_link0'

        self.detect_client = self.create_client(GetObjects, 'get_objects')
        self.gripper_client = self.create_client(SetBool, 'gripper_command')

        self.move_client = ActionClient(self, MoveToPose, '/goal_pose')

        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer, self)

        self.started = False
        self.timer = self.create_timer(0.5, self.start_once)

        self.current_done_callback = None

        self.approach_pose = None
        self.lower_pose = None
        self.lift_pose = None

        # Distance above the cylinder for the approach pose.
        self.approach_offset_z = 0.10

        # Distance to lift after gripping the cylinder.
        self.lift_offset_z = 0.008

        #Distance to push into the cylinder
        self.cylinder_push_offset_z =  0.018

        # Predefined pose before object detection.
        self.predefined_pose = PoseStamped()
        self.predefined_pose.header.frame_id = self.target_frame

        self.predefined_pose.pose.position.x = 0.3898
        self.predefined_pose.pose.position.y = -0.2290
        self.predefined_pose.pose.position.z = 0.59

        orientation = Rotation.from_euler('xyz', [0,0,90], degrees=True)
        q = orientation.as_quat()
        self.predefined_pose.pose.orientation.x = q[0]
        self.predefined_pose.pose.orientation.y = q[1]
        self.predefined_pose.pose.orientation.z = q[2]
        self.predefined_pose.pose.orientation.w = q[3]

        # Final predefined pose after dropping the cylinder.
        # Change these values to your desired final pose.
        self.final_pose = PoseStamped()
        self.final_pose.header.frame_id = self.target_frame

        self.final_pose.pose.position.x = 0.3898
        self.final_pose.pose.position.y = 0.0
        self.final_pose.pose.position.z = 0.4160

        final_orientation = Rotation.from_euler('xyz', [0, 0, 90], degrees=True)
        q_final = final_orientation.as_quat()
        self.final_pose.pose.orientation.x = q_final[0]
        self.final_pose.pose.orientation.y = q_final[1]
        self.final_pose.pose.orientation.z = q_final[2]
        self.final_pose.pose.orientation.w = q_final[3]

    def start_once(self):
        if self.started:
            return

        if not self.detect_client.wait_for_service(timeout_sec=0.1):
            self.get_logger().info('Waiting for get_objects service...')
            return

        if not self.gripper_client.wait_for_service(timeout_sec=0.1):
            self.get_logger().info('Waiting for gripper_command service...')
            return

        if not self.move_client.wait_for_server(timeout_sec=0.1):
            self.get_logger().info('Waiting for /goal_pose action server...')
            return

        self.started = True
        self.timer.cancel()

        self.get_logger().info('Moving to predefined pose before detection...')
        self.predefined_pose.header.stamp = self.get_clock().now().to_msg()

        self.send_move_goal(
            self.predefined_pose,
            done_callback=self.after_predefined_pose
        )

    def after_predefined_pose(self):
        self.get_logger().info('Predefined pose reached. Calling object detector...')

        request = GetObjects.Request()
        future = self.detect_client.call_async(request)
        future.add_done_callback(self.handle_detection_response)

    def handle_detection_response(self, future):
        try:
            response = future.result()
        except Exception as e:
            self.get_logger().error(f'Object detection service failed: {e}')
            rclpy.shutdown()
            return

        if not response.success:
            self.get_logger().error(f'Object detection failed: {response.message}')
            rclpy.shutdown()
            return

        pose_camera = response.object_pose

        # Use latest available TF.
        pose_camera.header.stamp = rclpy.time.Time().to_msg()

        self.get_logger().info(
            f'Received object pose in frame: {pose_camera.header.frame_id}'
        )

        try:
            grasp_pose = self.tf_buffer.transform(
                pose_camera,
                self.target_frame,
                timeout=Duration(seconds=1.0)
            )

        except Exception as e:
            self.get_logger().error(
                f'Could not transform pose from '
                f'{pose_camera.header.frame_id} to {self.target_frame}: {e}'
            )
            rclpy.shutdown()
            return

        # Create approach pose above the cylinder in the base frame.
        approach_pose = copy.deepcopy(grasp_pose)
        approach_pose.pose.position.z += self.approach_offset_z
        approach_pose.header.stamp = self.get_clock().now().to_msg()

        self.approach_pose = approach_pose

        self.get_logger().info(
            f'Moving to approach pose: '
            f'x={approach_pose.pose.position.x:.3f}, '
            f'y={approach_pose.pose.position.y:.3f}, '
            f'z={approach_pose.pose.position.z:.3f}'
        )

        self.send_move_goal(
            approach_pose,
            done_callback=self.after_approach_pose
        )

    def after_approach_pose(self):
        if self.approach_pose is None:
            self.get_logger().error('No approach pose stored. Cannot lower.')
            rclpy.shutdown()
            return

        lower_pose = copy.deepcopy(self.approach_pose)
        lower_pose.pose.position.z -= (self.approach_offset_z/2)
        lower_pose.header.stamp = self.get_clock().now().to_msg()

        self.lower_pose = lower_pose

        self.get_logger().info(
            f'Lowering onto cylinder: '
            f'x={lower_pose.pose.position.x:.3f}, '
            f'y={lower_pose.pose.position.y:.3f}, '
            f'z={lower_pose.pose.position.z:.3f}'
        )

        self.send_move_goal(
            lower_pose,
            done_callback=self.after_lower_pose
        )

    def after_lower_pose(self):
        if self.approach_pose is None:
            self.get_logger().error('No approach pose stored. Cannot lower.')
            rclpy.shutdown()
            return

        lower_pose2 = copy.deepcopy(self.lower_pose)
        lower_pose2.pose.position.z -= (self.approach_offset_z/2 + self.cylinder_push_offset_z)
        lower_pose2.header.stamp = self.get_clock().now().to_msg()

        self.lower_pose2 = lower_pose2

        self.get_logger().info(
            f'Lowering onto cylinder: '
            f'x={lower_pose2.pose.position.x:.3f}, '
            f'y={lower_pose2.pose.position.y:.3f}, '
            f'z={lower_pose2.pose.position.z:.3f}'
        )

        self.send_move_goal(
            lower_pose2,
            done_callback=self.after_lower2_pose
        )

    def after_lower2_pose(self):
        self.get_logger().info('Reached cylinder. Closing gripper...')

        self.send_gripper_command(
            close=True,
            done_callback=self.after_gripper_closed
        )

    def after_gripper_closed(self):
        if self.lower_pose is None:
            self.get_logger().error('No lower pose stored. Cannot lift.')
            rclpy.shutdown()
            return

        lift_pose = copy.deepcopy(self.lower_pose)
        lift_pose.pose.position.z += self.lift_offset_z
        lift_pose.header.stamp = self.get_clock().now().to_msg()

        self.lift_pose = lift_pose

        self.get_logger().info(
            f'Gripper closed. Lifting cylinder by {self.lift_offset_z:.3f} m: '
            f'x={lift_pose.pose.position.x:.3f}, '
            f'y={lift_pose.pose.position.y:.3f}, '
            f'z={lift_pose.pose.position.z:.3f}'
        )

        self.send_move_goal(
            lift_pose,
            done_callback=self.after_lift_pose
        )

    def after_lift_pose(self):
        self.get_logger().info('Lift completed. Opening gripper to drop cylinder...')

        self.send_gripper_command(
            close=False,
            done_callback=self.after_gripper_opened
        )

    def after_gripper_opened(self):
        self.get_logger().info('Cylinder dropped. Moving to final predefined pose...')

        self.final_pose.header.stamp = self.get_clock().now().to_msg()

        self.send_move_goal(
            self.final_pose,
            done_callback=self.after_final_pose
        )

    def after_final_pose(self):
        self.get_logger().info('Finished full pick/drop sequence.')
        rclpy.shutdown()

    def send_gripper_command(self, close: bool, done_callback):
        request = SetBool.Request()
        request.data = close

        command_name = 'CLOSE' if close else 'OPEN'
        self.get_logger().info(f'Sending gripper command: {command_name}')

        future = self.gripper_client.call_async(request)

        def handle_gripper_response(future):
            try:
                response = future.result()
            except Exception as e:
                self.get_logger().error(f'Gripper service call failed: {e}')
                rclpy.shutdown()
                return

            if not response.success:
                self.get_logger().error(
                    f'Gripper command {command_name} failed: {response.message}'
                )
                rclpy.shutdown()
                return

            self.get_logger().info(
                f'Gripper command {command_name} succeeded: {response.message}'
            )

            if done_callback is not None:
                done_callback()
            else:
                rclpy.shutdown()

        future.add_done_callback(handle_gripper_response)

    def send_move_goal(self, pose: PoseStamped, done_callback):
        goal = MoveToPose.Goal()
        goal.target_pose = pose

        self.current_done_callback = done_callback

        self.get_logger().info('Sending pose to MoveIt wrapper...')

        future = self.move_client.send_goal_async(
            goal,
            feedback_callback=self.feedback_callback
        )
        future.add_done_callback(self.handle_move_goal_response)

    def handle_move_goal_response(self, future):
        try:
            goal_handle = future.result()
        except Exception as e:
            self.get_logger().error(f'Failed to send move goal: {e}')
            rclpy.shutdown()
            return

        if not goal_handle.accepted:
            self.get_logger().error('Move goal rejected')
            rclpy.shutdown()
            return

        self.get_logger().info('Move goal accepted')

        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(self.handle_move_result)

    def handle_move_result(self, future):
        try:
            result = future.result().result
        except Exception as e:
            self.get_logger().error(f'Failed to get move result: {e}')
            rclpy.shutdown()
            return

        if not result.success:
            self.get_logger().error(
                f'Robot motion failed: {result.message}, '
                f'MoveIt code: {result.moveit_error_code}'
            )
            rclpy.shutdown()
            return

        self.get_logger().info('Robot motion completed successfully')

        callback = self.current_done_callback
        self.current_done_callback = None

        if callback is not None:
            callback()
        else:
            self.get_logger().info('No next callback. Shutting down.')
            rclpy.shutdown()

    def feedback_callback(self, feedback_msg):
        self.get_logger().info(f'MoveIt state: {feedback_msg.feedback.state}')


def main(args=None):
    rclpy.init(args=args)

    node = AutoPickUpExample()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Interrupted by user.')
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()