
import rclpy
from rclpy.node import Node
from std_srvs.srv import SetBool
from std_msgs.msg import Bool
from threading import Event

from gpiozero import DigitalInputDevice
from gpiozero import OutputDevice


#This node is responsible for gripper control, it has a service which listens for gripper close/open request, and it sets GPIO to HIGH for gripper lock request and LOW for gripper unlock request.
#On GPIO interrupt it publishes the new gripper state to the gripper/state topic.

#TODO: Add some form of timeout and error detection 

class GripperDriver(Node):

    def __init__(self):
        super().__init__('gripper_driver')
        self.publisher = self.create_publisher(Bool, "gripper/state", 10)
        self.srv = self.create_service(SetBool, 'gripper_command', self.gripper_command_callback)
        
        self.sensor_pin = DigitalInputDevice(17, pull_up=False, bounce_time=0.1) #Sensor pin from arduino is configured to GPIO 17
        self.lock_pin = OutputDevice(4)                                          #Pin for sending gripper lock command is configured to GPIO 4
        self.lock_pin.off()
        self.interrupt_event = Event()
        self.gripperClosed = self.sensor_pin.value #false -> gripper open | true -> gripper closed

        #Interrupt callbacks for sensor pin
        self.sensor_pin.when_activated = self.gripper_open
        self.sensor_pin.when_deactivated = self.gripper_closed

    #Publisher function for gripper sensor pin for 'gripper/state' topic
    def gripper_closed(self):
        msg = Bool()
        msg.data = True
        self.gripperClosed = True
        self.interrupt_event.set()
        self.get_logger().info("Gripper state changed: CLOSED")
        self.publisher.publish(msg)
    
    def gripper_open(self):
        msg = Bool()
        msg.data = False
        self.gripperClosed = False
        self.interrupt_event.set()
        self.get_logger().info("Gripper state changed: OPEN")
        self.publisher.publish(msg)

    #Service callback function sends lock/unlock signal to arduino on service request
    def gripper_command_callback(self, request, response):
        self.interrupt_event.clear()
        if(request.data):
            self.lock_pin.on()
            self.get_logger().info("Gripper command pin set: CLOSED")
            #Waits until the gripper state maches the requested state
            while(self.gripperClosed == False):
                self.interrupt_event.wait() #Wait for gripper to change state
                self.interrupt_event.clear()

            response.success = True
            response.message = "Gripper closed"
        
        elif(request.data != True):
            self.lock_pin.off()
            self.get_logger().info("Gripper command pin set: OPEN")
            #Waits until the gripper state maches the requested state
            while(self.gripperClosed == True):
                self.interrupt_event.wait() #Wait for gripper to change state
                self.interrupt_event.clear()

            response.success = True
            response.message = "Gripper open"
        
        return response


def main(args=None):
    rclpy.init(args=args)
    gripper_driver = GripperDriver()
    rclpy.spin(gripper_driver)
    gripper_driver.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()