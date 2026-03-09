
import rclpy
from rclpy.node import Node
from ri_seaweed_interfaces.msg import Gripper

class GripperController(Node):

    def __init__(self):
        super().__init__('gripper_controller')
        self.publisher = self.create_publisher(Gripper, 'gripper', 10)
        timer_period = 8
        self.close_request = True
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):
        self.get_logger().info("timer tick")
        msg = Gripper()
        if(self.close_request == True):
            msg.close_request = True
            self.close_request = False
        elif(self.close_request == False):
            msg.close_request = False
            self.close_request = True

        self.publisher.publish(msg)


def main(args=None):
    rclpy.init(args=args)

    gripper_controller = GripperController()

    rclpy.spin(gripper_controller)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    gripper_controller.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()


