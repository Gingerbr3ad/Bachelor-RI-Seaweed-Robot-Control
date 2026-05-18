import time
import csv

import rclpy
from rclpy.node import Node

from ri_seaweed_interfaces.srv import GetObjects


class GetObjectsServiceTimer(Node):
    """
    ROS 2 node for measuring response time of the get_objects service.

    Behavior:
        - Calls the get_objects service 30 times.
        - Measures the time from sending the request until receiving the response.
        - Stores all measurements in an array.
        - Saves the measurements to a CSV file.
        - Stops automatically after 30 measurements.
    """

    def __init__(self):
        super().__init__('get_objects_service_timer')

        self.client = self.create_client(GetObjects, 'get_objects')

        self.max_measurements = 30
        self.measurements_ms = []
        self.csv_filename = "get_objects_service_times.csv"

        self.get_logger().info("Waiting for get_objects service...")

        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("Service not available, waiting...")

        self.get_logger().info("get_objects service is available.")
        self.get_logger().info("Starting service response time measurements.")

    def run_measurements(self):
        """
        Calls the service repeatedly and measures response time.
        """
        for measurement_number in range(1, self.max_measurements + 1):
            request = GetObjects.Request()

            start_time_ns = time.perf_counter_ns()

            future = self.client.call_async(request)

            rclpy.spin_until_future_complete(self, future)

            end_time_ns = time.perf_counter_ns()

            response_time_ms = (end_time_ns - start_time_ns) / 1_000_000.0
            self.measurements_ms.append(response_time_ms)

            if future.result() is not None:
                response = future.result()

                self.get_logger().info(
                    f"Measurement {measurement_number}/{self.max_measurements}: "
                    f"response time = {response_time_ms:.3f} ms | "
                    f"success = {response.success} | "
                    f"message = {response.message}"
                )
            else:
                self.get_logger().error(
                    f"Measurement {measurement_number}/{self.max_measurements}: "
                    f"service call failed after {response_time_ms:.3f} ms"
                )

        self.save_measurements_to_csv()
        self.print_statistics()

    def save_measurements_to_csv(self):
        """
        Saves all response time measurements to a CSV file.
        """
        with open(self.csv_filename, mode="w", newline="") as csv_file:
            writer = csv.writer(csv_file)

            writer.writerow(["measurement_number", "response_time_ms"])

            for index, response_time_ms in enumerate(self.measurements_ms, start=1):
                writer.writerow([index, response_time_ms])

        self.get_logger().info(
            f"Saved {len(self.measurements_ms)} measurements to {self.csv_filename}"
        )

    def print_statistics(self):
        """
        Prints simple timing statistics.
        """
        if not self.measurements_ms:
            self.get_logger().warn("No measurements were recorded.")
            return

        average_ms = sum(self.measurements_ms) / len(self.measurements_ms)
        minimum_ms = min(self.measurements_ms)
        maximum_ms = max(self.measurements_ms)

        self.get_logger().info("Finished all service timing measurements.")
        self.get_logger().info(f"Service response times in ms:")
        self.get_logger().info(str(self.measurements_ms))

        self.get_logger().info(f"Average response time: {average_ms:.3f} ms")
        self.get_logger().info(f"Minimum response time: {minimum_ms:.3f} ms")
        self.get_logger().info(f"Maximum response time: {maximum_ms:.3f} ms")


def main(args=None):
    rclpy.init(args=args)

    service_timer = GetObjectsServiceTimer()

    try:
        service_timer.run_measurements()
    except KeyboardInterrupt:
        pass
    finally:
        service_timer.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()