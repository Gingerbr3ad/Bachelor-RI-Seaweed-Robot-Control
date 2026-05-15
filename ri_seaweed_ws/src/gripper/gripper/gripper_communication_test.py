import rclpy
from rclpy.node import Node

from gpiozero import DigitalInputDevice
from gpiozero import OutputDevice


class GripperCommunicationTester(Node):
    """
    ROS 2 node for testing GPIO communication with an Arduino.

    Behavior:
        - Every 3 seconds, flips the output pin ON/OFF.
        - Logs the output pin state.
        - Reads and logs the input pin state.
    """

    def __init__(self):
        super().__init__('gripper_communication_tester')

        # GPIO setup
        self.input_pin = DigitalInputDevice(17, pull_up=False, bounce_time=0.3)
        self.output_pin = OutputDevice(4)

        self.output_state = False
        self.output_pin.off()

        self.timer_period = 5.0
        self.timer = self.create_timer(self.timer_period, self.timer_callback)

        self.get_logger().info("Gripper_communication_tester started")
        self.log_gpio_states()

    def timer_callback(self):
        """
        Flip output pin every timer tick and log both GPIO states.
        """
        self.output_state = not self.output_state

        if self.output_state:
            self.output_pin.on()
        else:
            self.output_pin.off()

        self.log_gpio_states()

    def log_gpio_states(self):
        output_text = "ON" if self.output_state else "OFF"
        input_state = bool(self.input_pin.value)
        input_text = "HIGH" if input_state else "LOW"

        self.get_logger().info(
            f"Output pin state: {output_text} | "
            f"Input pin state: {input_text}"
        )

    def destroy_node(self):

        try:
            self.output_pin.off()
            self.input_pin.close()
            self.output_pin.close()
        finally:
            super().destroy_node()


def main(args=None):
    rclpy.init(args=args)

    gripper_communication_tester = GripperCommunicationTester()

    try:
        rclpy.spin(gripper_communication_tester)
    except KeyboardInterrupt:
        pass
    finally:
        gripper_communication_tester.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()