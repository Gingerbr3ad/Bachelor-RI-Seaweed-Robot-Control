#Based on the Franka code of Jakobs colleague, need to credit him!

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from rclpy.action import ActionServer
from rclpy.executors import MultiThreadedExecutor
from threading import Event

from moveit_msgs.action import MoveGroup
from moveit_msgs.msg import (
    MotionPlanRequest,
    Constraints,
    PositionConstraint,
    OrientationConstraint,
    BoundingVolume,
    WorkspaceParameters,
    PlanningOptions,
)
from geometry_msgs.msg import PoseStamped
from shape_msgs.msg import SolidPrimitive

from ri_seaweed_interfaces.action import MoveToPose

# Planning tolerances [m]
ORIENTATION_TOLERANCE = 0.01
TRANSLATEION_TOLERACNE = [0.001] 


class KukaMoveItCommander(Node):
    def __init__(self):
        super().__init__('kuka_moveit_commander')

        # MoveIt action server
        self._action_client = ActionClient(self, MoveGroup, '/move_action')
        self._action_server = ActionServer(self, MoveToPose, '/goal_pose', self.execute_callback)

        # KUKA repo defaults
        self.planning_group = 'manipulator'
        self.end_effector_link = 'flange'
        self.base_frame = 'base_link'

        self._moveit_done_event = Event()

    def send_pose_goal(self, x, y, z, qx=0.0, qy=0.0, qz=0.0, qw=1.0):
        self.get_logger().info('Waiting for MoveGroup action server...')
        self._action_client.wait_for_server()

        goal_msg = MoveGroup.Goal()

        request = MotionPlanRequest()
        request.group_name = self.planning_group
        request.num_planning_attempts = 10
        request.allowed_planning_time = 5.0
        request.max_velocity_scaling_factor = 0.2
        request.max_acceleration_scaling_factor = 0.2

        # Workspace
        request.workspace_parameters = WorkspaceParameters()
        request.workspace_parameters.header.frame_id = self.base_frame
        request.workspace_parameters.min_corner.x = -2.0
        request.workspace_parameters.min_corner.y = -2.0
        request.workspace_parameters.min_corner.z = -0.5
        request.workspace_parameters.max_corner.x = 2.0
        request.workspace_parameters.max_corner.y = 2.0
        request.workspace_parameters.max_corner.z = 2.0

        # Target pose
        target_pose = PoseStamped()
        target_pose.header.frame_id = self.base_frame
        target_pose.pose.position.x = x
        target_pose.pose.position.y = y
        target_pose.pose.position.z = z
        target_pose.pose.orientation.x = qx
        target_pose.pose.orientation.y = qy
        target_pose.pose.orientation.z = qz
        target_pose.pose.orientation.w = qw

        # Position constraint
        position_constraint = PositionConstraint()
        position_constraint.header.frame_id = self.base_frame
        position_constraint.link_name = self.end_effector_link
        position_constraint.target_point_offset.x = 0.0
        position_constraint.target_point_offset.y = 0.0
        position_constraint.target_point_offset.z = 0.0

        bounding_volume = BoundingVolume()
        sphere = SolidPrimitive()
        sphere.type = SolidPrimitive.SPHERE
        sphere.dimensions = TRANSLATEION_TOLERACNE
        bounding_volume.primitives.append(sphere)
        bounding_volume.primitive_poses.append(target_pose.pose)

        position_constraint.constraint_region = bounding_volume
        position_constraint.weight = 1.0

        # Orientation constraint
        orientation_constraint = OrientationConstraint()
        orientation_constraint.header.frame_id = self.base_frame
        orientation_constraint.link_name = self.end_effector_link
        orientation_constraint.orientation = target_pose.pose.orientation
        orientation_constraint.absolute_x_axis_tolerance = ORIENTATION_TOLERANCE
        orientation_constraint.absolute_y_axis_tolerance = ORIENTATION_TOLERANCE
        orientation_constraint.absolute_z_axis_tolerance = ORIENTATION_TOLERANCE
        orientation_constraint.weight = 1.0

        # Goal constraints
        constraints = Constraints()
        constraints.position_constraints.append(position_constraint)
        constraints.orientation_constraints.append(orientation_constraint)
        request.goal_constraints.append(constraints)

        goal_msg.request = request

        # Planning options
        goal_msg.planning_options = PlanningOptions()
        goal_msg.planning_options.plan_only = False
        goal_msg.planning_options.replan = True
        goal_msg.planning_options.replan_attempts = 5

        self.get_logger().info(
            f"Sending goal for group={self.planning_group}, "
            f"link={self.end_effector_link}, "
            f"pose=({x:.3f}, {y:.3f}, {z:.3f})"
        )

        send_goal_future = self._action_client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback
        )
        send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()

        if not goal_handle.accepted:
            self.get_logger().error('MoveIt goal rejected')
            self._moveit_success = False
            self._moveit_error_code = -1
            self._moveit_message = 'MoveIt goal rejected'
            self._moveit_done = True
            return

        self.get_logger().info('MoveIt goal accepted')

        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(self.result_callback)

    def result_callback(self, future):
        result = future.result().result
        self._moveit_error_code = result.error_code.val

        if result.error_code.val == 1:
            self._moveit_success = True
            self._moveit_message = 'Motion completed successfully'
            self.get_logger().info(self._moveit_message)
        else:
            self._moveit_success = False
            self._moveit_message = (
                f'Motion failed with MoveIt error code: {result.error_code.val}'
            )
            self.get_logger().error(self._moveit_message)

        self._moveit_done = True
        self._moveit_done_event.set()

    def feedback_callback(self, feedback_msg):
        state = feedback_msg.feedback.state
        self.get_logger().info(f"MoveIt state: {state}")

        if hasattr(self, '_wrapper_goal_handle') and self._wrapper_goal_handle is not None:
            feedback = MoveToPose.Feedback()
            feedback.state = state
            self._wrapper_goal_handle.publish_feedback(feedback)


    def execute_callback(self, goal_handle):
        self._wrapper_goal_handle = goal_handle
        self._moveit_done = False
        self._moveit_success = False
        self._moveit_error_code = 0
        self._moveit_message = ''
        self._moveit_done_event.clear()

        pose = goal_handle.request.target_pose

        self.send_pose_goal(
            pose.pose.position.x,
            pose.pose.position.y,
            pose.pose.position.z,
            pose.pose.orientation.x,
            pose.pose.orientation.y,
            pose.pose.orientation.z,
            pose.pose.orientation.w
        )

        self._moveit_done_event.wait()       

        result = MoveToPose.Result()
        result.success = self._moveit_success
        result.message = self._moveit_message
        result.moveit_error_code = self._moveit_error_code

        if self._moveit_success:
            goal_handle.succeed()
        else:
            goal_handle.abort()

        return result




def main(args=None):
    rclpy.init(args=args)
    kuka_moveit_commander = KukaMoveItCommander()
    executor = MultiThreadedExecutor(num_threads=2)
    executor.add_node(kuka_moveit_commander)
    executor.spin()
    executor.shutdown()
    kuka_moveit_commander.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()