import rclpy
from rclpy.node import Node
from rclpy.logging import LoggingSeverity
from std_srvs.srv import SetBool


#This is a dummy gripper controller node, it periodically sends lock/unlock requests to the gripper_command service.
#The purpouse of this node is to test the gripper driver node without the rest of the system for legitimate gripper lock/unlock calls.

class GripperDummyController(Node):

    def __init__(self):
        super().__init__('gripper_dummy_controller')
        self.cli = self.create_client(SetBool, 'gripper_command')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        
        timer_period = 6 # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

        self.close_command = False

    #Sends the lock/unlock request on timer callback
    def timer_callback(self):
        request = SetBool.Request()

        if(self.close_command == False):
            self.close_command = True
            self.get_logger().debug("Dummy gripper command: CLOSE")
        elif(self.close_command == True):
            self.close_command = False
            self.get_logger().debug("Dummy gripper command: OPEN")
        
        request.data = self.close_command
        self.cli.call_async(request)
    
    #Sets the node default logging to DEBUG level
    rclpy.logging.set_logger_level('gripper_dummy_controller', LoggingSeverity.DEBUG)

            


def main(args=None):
    rclpy.init(args=args)
    gripper_dummy_controller = GripperDummyController()
    rclpy.spin(gripper_dummy_controller)
    gripper_dummy_controller.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
