import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from rclpy.duration import Duration

import tf2_ros
import tf2_geometry_msgs  # needed for PoseStamped TF support

from geometry_msgs.msg import PoseStamped
from ri_seaweed_interfaces.srv import GetObjects
from ri_seaweed_interfaces.action import MoveToPose


class DetectTransformMove(Node):
    def __init__(self):
        super().__init__('detect_transform_move')

        self.target_frame = 'base_link'  # or 'world' if that is your MoveIt frame

        self.detect_client = self.create_client(GetObjects, 'get_objects')
        self.move_client = ActionClient(self, MoveToPose, '/goal_pose')

        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer, self)

        self.started = False
        self.timer = self.create_timer(0.5, self.start_once)

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

        self.get_logger().info('Calling object detector...')
        request = GetObjects.Request()
        future = self.detect_client.call_async(request)
        future.add_done_callback(self.handle_detection_response)

    def handle_detection_response(self, future):
        try:
            response = future.result()
        except Exception as e:
            self.get_logger().error(f'Object detection service failed: {e}')
            return

        if not response.success:
            self.get_logger().error(f'Object detection failed: {response.message}')
            return

        pose_camera = response.object_pose

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
            return

        self.get_logger().info(
            f'Transformed pose to {self.target_frame}: '
            f'x={pose_base.pose.position.x:.3f}, '
            f'y={pose_base.pose.position.y:.3f}, '
            f'z={pose_base.pose.position.z:.3f}'
        )

        self.send_move_goal(pose_base)

    def send_move_goal(self, pose: PoseStamped):
        goal = MoveToPose.Goal()
        goal.target_pose = pose

        self.get_logger().info('Sending pose to MoveIt wrapper...')

        future = self.move_client.send_goal_async(
            goal,
            feedback_callback=self.feedback_callback
        )
        future.add_done_callback(self.handle_move_goal_response)

    def handle_move_goal_response(self, future):
        goal_handle = future.result()

        if not goal_handle.accepted:
            self.get_logger().error('Move goal rejected')
            return

        self.get_logger().info('Move goal accepted')

        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(self.handle_move_result)

    def handle_move_result(self, future):
        result = future.result().result

        if result.success:
            self.get_logger().info('Robot motion completed successfully')
        else:
            self.get_logger().error(
                f'Robot motion failed: {result.message}, '
                f'MoveIt code: {result.moveit_error_code}'
            )

        rclpy.shutdown()

    def feedback_callback(self, feedback_msg):
        self.get_logger().info(f'MoveIt state: {feedback_msg.feedback.state}')


def main(args=None):
    rclpy.init(args=args)
    node = DetectTransformMove()
    rclpy.spin(node)


if __name__ == '__main__':
    main()
