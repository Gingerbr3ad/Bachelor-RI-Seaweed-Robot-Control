import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient

from geometry_msgs.msg import PoseStamped
from ri_seaweed_interfaces.action import MoveToPose

from scipy.spatial.transform import Rotation


class MotionExample(Node):
    def __init__(self):
        super().__init__('three_waypoint_mover')

        self.target_frame = 'fr3_link0'
        self.move_client = ActionClient(self, MoveToPose, '/goal_pose')

        self.started = False
        self.timer = self.create_timer(0.5, self.start_once)

        self.home = PoseStamped()
        self.home.header.frame_id = self.target_frame

        self.home.pose.position.x = 0.3898
        self.home.pose.position.y = 0.0
        self.home.pose.position.z = 0.4160

        orientation3 = Rotation.from_euler('xyz', [0,0,90], degrees=True)
        q3 = orientation3.as_quat()
        self.home.pose.orientation.x = q3[0]
        self.home.pose.orientation.y = q3[1]
        self.home.pose.orientation.z = q3[2]
        self.home.pose.orientation.w = q3[3]
        #######################################

    #Start the sequence after the timer expires
    def start_once(self):
        if self.started:
            return

        if not self.move_client.wait_for_server(timeout_sec=0.1):
            self.get_logger().info('Waiting for /goal_pose action server...')
            return

        self.started = True
        self.timer.cancel()

        self.send_move_goal(self.home, done_callback=self.after_home) # Send the goal of the 1st waypoint to the MoveIt Commander and sets a callback function for after the motion is done
        self.get_logger().info('Moving home...')
    
    def after_home(self):
        self.get_logger().info('Arrived home')
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

    node = MotionExample()

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