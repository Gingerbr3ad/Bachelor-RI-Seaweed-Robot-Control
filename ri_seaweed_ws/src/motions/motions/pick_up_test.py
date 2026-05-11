import copy

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from rclpy.duration import Duration

import tf2_ros
import tf2_geometry_msgs  # needed for PoseStamped TF support

from geometry_msgs.msg import PoseStamped
from ri_seaweed_interfaces.srv import GetObjects
from ri_seaweed_interfaces.action import MoveToPose

from scipy.spatial.transform import Rotation


class DetectTransformMove(Node):
    def __init__(self):
        super().__init__('detect_transform_move')

        self.target_frame = 'fr3_link0'

        self.detect_client = self.create_client(GetObjects, 'get_objects')
        self.move_client = ActionClient(self, MoveToPose, '/goal_pose')

        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer, self)

        self.started = False
        self.timer = self.create_timer(0.5, self.start_once)

        self.current_done_callback = None
        self.approach_pose = None

        # Distance above the cylinder for the approach pose.
        # The robot will later lower by this same distance.
        self.approach_offset_z = 0.2

        # Predefined pose before object detection.
        # Adjust these values for your robot/workspace.
        self.predefined_pose = PoseStamped()
        self.predefined_pose.header.frame_id = self.target_frame

        self.predefined_pose.pose.position.x = 0.3898
        self.predefined_pose.pose.position.y = -0.2290
        self.predefined_pose.pose.position.z = 0.7260
        
        orientation = Rotation.from_euler('xyz', [179, 0, 45], degrees=True)
        q = orientation.as_quat()
        self.predefined_pose.pose.orientation.x = q[0]
        self.predefined_pose.pose.orientation.y = q[1]
        self.predefined_pose.pose.orientation.z = q[2]
        self.predefined_pose.pose.orientation.w = q[3]

    def start_once(self):
        if self.started:
            return

        if not self.detect_client.wait_for_service(timeout_sec=0.1):
            self.get_logger().info('Waiting for get_objects service...')
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
            pose_base = self.tf_buffer.transform(
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

        self.get_logger().info(
            f'Detected cylinder pose in {self.target_frame}: '
            f'x={pose_base.pose.position.x:.3f}, '
            f'y={pose_base.pose.position.y:.3f}, '
            f'z={pose_base.pose.position.z:.3f}'
        )

        # Create approach pose above the cylinder in the base frame.
        approach_pose = copy.deepcopy(pose_base)
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
        lower_pose.pose.position.z -= 0.070
        lower_pose.header.stamp = self.get_clock().now().to_msg()

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
        self.get_logger().info('Finished lowering onto cylinder.')
        rclpy.shutdown()

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

    node = DetectTransformMove()

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