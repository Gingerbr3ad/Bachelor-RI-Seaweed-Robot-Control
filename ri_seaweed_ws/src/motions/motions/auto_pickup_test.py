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

class AutoPickup(Node):
    def __init__(self):
        super().__init__('auto_pickup')

        self.move_client = ActionClient(self, MoveToPose, '/goal_pose')

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
    node = AutoPickup()
    camera_pose = PoseStamped()    
    camera_pose.header.stamp = node.get_clock().now().to_msg()
    camera_pose.header.frame_id = "base_frame"

    camera_pose.pose.position.x = 0.3898
    camera_pose.pose.position.y = -0.2290
    camera_pose.pose.position.z = 0.7260
    
    orientation = Rotation.from_euler('xyz', [179, 0, 45], degrees=True)
    q = orientation.as_quat()
    camera_pose.pose.orientation.x = q[0]
    camera_pose.pose.orientation.y = q[1]
    camera_pose.pose.orientation.z = q[2]
    camera_pose.pose.orientation.w = q[3]

    if not node.move_client.wait_for_server(timeout_sec=5.0):
        node.get_logger().error("MoveToPose action server /goal_pose not available")
        rclpy.shutdown()
        return

    node.send_move_goal(camera_pose)
    rclpy.spin(node)


if __name__ == '__main__':
    main()
