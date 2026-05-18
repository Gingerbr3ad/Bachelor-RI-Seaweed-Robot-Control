import time
from threading import Event, Lock

import rclpy
from rclpy.node import Node
from std_srvs.srv import SetBool
from std_msgs.msg import Bool

from gpiozero import DigitalInputDevice
from gpiozero import OutputDevice


class GripperDriver(Node):
    """
    ROS 2 node for controlling a simple lock/unlock gripper.

    Service:
        /gripper_command [std_srvs/SetBool]
            request.data == True  -> close / lock gripper
            request.data == False -> open / unlock gripper

    Publisher:
        /gripper/state [std_msgs/Bool]
            True  -> gripper closed
            False -> gripper open
    """

    def __init__(self):
        super().__init__('gripper_driver')

        self.publisher = self.create_publisher(Bool, "gripper/state", 10)
        self.srv = self.create_service(SetBool, 'gripper_command', self.gripper_command_callback)
        self.get_logger().info(f"Gripper Driver started")

        self.command_timeout = 5.0

        # GPIO setup
        self.sensor_pin = DigitalInputDevice(17, pull_up=False, bounce_time=0.3)
        self.lock_pin = OutputDevice(4)
        self.lock_pin.off()

        self.state_event = Event()
        self.state_lock = Lock()

        # sensor_pin.value == False -> gripper open
        # sensor_pin.value == True  -> gripper closed
        self.gripper_closed_state = bool(self.sensor_pin.value)

        # Interrupt callbacks for sensor pin.
        self.sensor_pin.when_activated = self.gripper_closed
        self.sensor_pin.when_deactivated = self.gripper_open

        self.get_logger().info(f"Initial gripper state: " f"{'CLOSED' if self.gripper_closed_state else 'OPEN'}")
        self.publish_gripper_state(self.gripper_closed_state)

    def publish_gripper_state(self, is_closed: bool):
        msg = Bool()
        msg.data = is_closed
        self.publisher.publish(msg)

    def set_gripper_state(self, is_closed: bool):
        with self.state_lock:
            self.gripper_closed_state = is_closed

        self.state_event.set()

        state_text = "CLOSED" if is_closed else "OPEN"
        self.get_logger().info(f"Gripper state changed: {state_text}")
        self.publish_gripper_state(is_closed)

    def gripper_closed(self):
        self.set_gripper_state(True)

    def gripper_open(self):
        self.set_gripper_state(False)

    def get_current_state(self) -> bool:
        with self.state_lock:
            return self.gripper_closed_state

    def wait_for_state(self, target_closed: bool) -> bool:
        """
        Wait until the gripper state matches target_closed.

        Returns True if target state was reached, False on timeout.
        """
        deadline = time.monotonic() + self.command_timeout

        while rclpy.ok():
            if self.get_current_state() == target_closed:
                return True

            remaining_time = deadline - time.monotonic()
            if remaining_time <= 0.0:
                return False

            self.state_event.wait(timeout=remaining_time)
            self.state_event.clear()

        return False

    def gripper_command_callback(self, request, response):
        target_closed = bool(request.data)

        self.state_event.clear()

        if target_closed:
            self.lock_pin.on()
            self.get_logger().info("Gripper command pin set: CLOSE")
        else:
            self.lock_pin.off()
            self.get_logger().info("Gripper command pin set: OPEN")

        success = self.wait_for_state(target_closed)

        current_state = self.get_current_state()
    
        if success:
            response.success = True
            response.message = (
                "Gripper closed"
                if target_closed
                else "Gripper open"
            )
        else:
            response.success = False
            if current_state:
                self.lock_pin.on()
            else:
                self.lock_pin.off()
            response.message = (
                f"Timeout waiting for gripper to "
                f"{'close' if target_closed else 'open'}. "
                f"Current state is "
                f"{'closed' if current_state else 'open'}."
            )

            self.get_logger().error(response.message)

        return response

    def destroy_node(self):
        self.get_logger().info("Shutting down gripper driver")

        try:
            self.lock_pin.off()
            self.sensor_pin.close()
            self.lock_pin.close()
        finally:
            super().destroy_node()


def main(args=None):
    rclpy.init(args=args)

    gripper_driver = GripperDriver()

    try:
        rclpy.spin(gripper_driver)
    except KeyboardInterrupt:
        pass
    finally:
        gripper_driver.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()