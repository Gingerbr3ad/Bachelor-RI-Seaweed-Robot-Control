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
        self.move_client = ActionClient(self, MoveToPose, '/goal_pose') # Create the action client for the MoveIt Commander action server

        self.started = False
        self.timer = self.create_timer(0.5, self.start_once) # Timer that will start the motion sequence 

        # Here we create out predefined waypoints
        self.waypoint1 = PoseStamped()
        self.waypoint1.header.frame_id = self.target_frame

        self.waypoint1.pose.position.x = 0.4898
        self.waypoint1.pose.position.y = 0.2290
        self.waypoint1.pose.position.z = 0.59

        orientation1 = Rotation.from_euler('xyz', [0,0,90], degrees=True)
        q1 = orientation1.as_quat()
        self.waypoint1.pose.orientation.x = q1[0]
        self.waypoint1.pose.orientation.y = q1[1]
        self.waypoint1.pose.orientation.z = q1[2]
        self.waypoint1.pose.orientation.w = q1[3]
        ########################################
        self.waypoint2 = PoseStamped()
        self.waypoint2.header.frame_id = self.target_frame

        self.waypoint2.pose.position.x = 0.2898
        self.waypoint2.pose.position.y = -0.2290
        self.waypoint2.pose.position.z = 0.39

        orientation2 = Rotation.from_euler('xyz', [0,0,90], degrees=True)
        q2 = orientation2.as_quat()
        self.waypoint2.pose.orientation.x = q2[0]
        self.waypoint2.pose.orientation.y = q2[1]
        self.waypoint2.pose.orientation.z = q2[2]
        self.waypoint2.pose.orientation.w = q2[3]
        #######################################
        self.waypoint3 = PoseStamped()
        self.waypoint3.header.frame_id = self.target_frame

        self.waypoint3.pose.position.x = 0.3898
        self.waypoint3.pose.position.y = 0.0
        self.waypoint3.pose.position.z = 0.4160

        orientation3 = Rotation.from_euler('xyz', [0,0,90], degrees=True)
        q3 = orientation3.as_quat()
        self.waypoint3.pose.orientation.x = q3[0]
        self.waypoint3.pose.orientation.y = q3[1]
        self.waypoint3.pose.orientation.z = q3[2]
        self.waypoint3.pose.orientation.w = q3[3]
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

        self.get_logger().info('Starting 3-waypoint motion sequence...') 
        self.send_move_goal(self.waypoint1, done_callback=self.after_waypoint1) # Send the goal of the 1st waypoint to the MoveIt Commander and sets a callback function for after the motion is done
        self.get_logger().info('Moving to waypoint 1')

    def after_waypoint1(self):
        self.send_move_goal(self.waypoint2, done_callback=self.after_waypoint2) # Send the goal of the 2nd waypoint to the MoveIt Commander after the 2st motion is done
        self.get_logger().info('Moving to waypoint 2')

    def after_waypoint2(self):
        self.send_move_goal(self.waypoint3, done_callback=self.after_waypoint3) # Send the goal of the 2nd waypoint to the MoveIt Commander after the 2st motion is done
        self.get_logger().info('Moving to waypoint 3')
        
    def after_waypoint3(self):
        self.get_logger().info('Sequence finished')                             # Log a message after the 3rd motion is done
        rclpy.shutdown()




    # Here we define the function for sending the goal pose to the MoveIt Commander
    # This can be either used as an example, or simply copy pasted into new nodes
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