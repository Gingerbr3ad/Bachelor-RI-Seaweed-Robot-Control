import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool

class GripperDummyController(Node):

    def __init__(self):
        super().__init__('gripper_dummy_controller')
        self.publisher_ = self.create_publisher(Bool, 'gripper/close_command', 10)
        timer_period = 5 # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

        self.close_commad = False

    def timer_callback(self):
        msg = Bool()

        if(self.close_commad == False):
            self.close_commad = True
        elif(self.close_commad == True):
            self.close_commad = False
        
        msg.data = self.close_commad
        self.publisher_.publish(msg)

            


def main(args=None):
    rclpy.init(args=args)

    gripper_dummy_controller = GripperDummyController()

    rclpy.spin(gripper_dummy_controller)

    gripper_dummy_controller.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
