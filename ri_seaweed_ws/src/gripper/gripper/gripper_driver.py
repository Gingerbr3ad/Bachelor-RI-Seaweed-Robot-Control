
import rclpy
from rclpy.node import Node
from ri_seaweed_interfaces.msg import Gripper
from std_msgs.msg import Bool

from gpiozero import DigitalInputDevice
from gpiozero import OutputDevice


#This node is responsible for gripper control, it has a subscriber which listens for gripper close/open command, and it sends the HIGH for girpper lock command and LOW for gripper unlock command on listener callback.
#It also has a publisher updates the 'gripper/state' topicon interrupts from the gripper sensor pin

class GripperDriver(Node):

    def __init__(self):
        super().__init__('gripper_driver')
        self.publisher = self.create_publisher(Bool, "gripper/state", 10)
        self.subscription = self.create_subscription(Bool, 'gripper/close_command', self.listener_callback, 10)
        self.subscription #Avoids 'vaiable unused' warning
        
        self.sensor_pin = DigitalInputDevice(17, pull_up=False) #Sensor pin from arduino is configured to GPIO 17
        self.lock_pin = OutputDevice(4)                         #Pin for sending gripper lock command is configured to GPIO 4
        self.lock_pin.off()

        #Interrupt callbacks for sensor pin
        self.sensor_pin.when_activated = self.gripper_closed
        self.sensor_pin.when_deactivated = self.gripper_open

    #Publisher function for gripper sensor pin for 'gripper/state' topic
    def gripper_closed(self):
        msg = Bool()
        msg.data = True
        self.get_logger().info("Gripper state changed: CLOSED")
        self.publisher.publish(msg)
    
    def gripper_open(self):
        msg = Bool()
        msg.data = False
        self.get_logger().info("Gripper state changed: OPEN")
        self.publisher.publish(msg)
    
    #Listener callback function sends lock/unlock signal to arduino on change in 'gripper/close_command' topic
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