
import rclpy
from rclpy.node import Node
from ri_seaweed_interfaces.msg import Gripper
from std_msgs.msg import Bool

from gpiozero import DigitalInputDevice
from gpiozero import OutputDevice

class GripperDriver(Node):

    def __init__(self):
        super().__init__('gripper_driver')
        self.publisher = self.create_publisher(Bool, "gripper/state", 10)
        self.subscription = self.create_subscription(Bool, 'gripper/close_command', self.listener_callback, 10)
        self.subscription
        
        self.sensor_pin = DigitalInputDevice(17, pull_up=False)
        self.lock_pin = OutputDevice(4)
        self.lock_pin.off()

        self.sensor_pin.when_activated = self.gripper_closed
        self.sensor_pin.when_deactivated = self.gripper_open

    def gripper_closed(self):
        msg = Bool()
        msg.data = True
        self.publisher.publish(msg)
    
    def gripper_open(self):
        msg = Bool()
        msg.data = False
        self.publisher.publish(msg)
    
    def listener_callback(self, msg):
        if(msg.data):
            self.lock_pin.on()

        elif (msg.data != True):
            self.lock_pin.off()


def main(args=None):
    rclpy.init(args=args)

    gripper_driver = GripperDriver()

    rclpy.spin(gripper_driver)
    gripper_driver.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()