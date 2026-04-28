import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from moveit_msgs.action import MoveGroup
from moveit_msgs.msg import (
    MotionPlanRequest,
    Constraints,
    PositionConstraint,
    OrientationConstraint,
    BoundingVolume,
    WorkspaceParameters,
)
from geometry_msgs.msg import PoseStamped
from shape_msgs.msg import SolidPrimitive


class MoveItCommander(Node):
    def __init__(self):
        super().__init__('moveit_commander')
        self._action_client = ActionClient(self, MoveGroup, '/move_action')
        
        # Configure for Franka - adjust these if needed
        self.planning_group = 'fr3_arm'
        self.end_effector_link = 'fr3_link8'
        self.base_frame = 'fr3_link0'

    def send_pose_goal(self, x, y, z, qx=0.0, qy=0.0, qz=0.0, qw=1.0):
        """Send a pose goal to MoveIt."""
        self.get_logger().info('Waiting for MoveGroup action server...')
        self._action_client.wait_for_server()

        goal_msg = MoveGroup.Goal()
        
        # Motion plan request
        request = MotionPlanRequest()
        request.group_name = self.planning_group
        request.num_planning_attempts = 10
        request.allowed_planning_time = 5.0
        request.max_velocity_scaling_factor = 0.3
        request.max_acceleration_scaling_factor = 0.3

        # Workspace parameters
        request.workspace_parameters = WorkspaceParameters()
        request.workspace_parameters.header.frame_id = self.base_frame
        request.workspace_parameters.min_corner.x = -1.0
        request.workspace_parameters.min_corner.y = -1.0
        request.workspace_parameters.min_corner.z = -1.0
        request.workspace_parameters.max_corner.x = 1.0
        request.workspace_parameters.max_corner.y = 1.0
        request.workspace_parameters.max_corner.z = 1.0

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

        # Bounding volume for position tolerance
        bounding_volume = BoundingVolume()
        solid = SolidPrimitive()
        solid.type = SolidPrimitive.SPHERE
        solid.dimensions = [0.005]  # 1cm tolerance
        bounding_volume.primitives.append(solid)
        bounding_volume.primitive_poses.append(target_pose.pose)
        position_constraint.constraint_region = bounding_volume
        position_constraint.weight = 1.0

        # Orientation constraint
        orientation_constraint = OrientationConstraint()
        orientation_constraint.header.frame_id = self.base_frame
        orientation_constraint.link_name = self.end_effector_link
        orientation_constraint.orientation = target_pose.pose.orientation
        orientation_constraint.absolute_x_axis_tolerance = 0.01
        orientation_constraint.absolute_y_axis_tolerance = 0.01
        orientation_constraint.absolute_z_axis_tolerance = 0.01
        orientation_constraint.weight = 1.0

        # Add constraints to goal
        constraints = Constraints()
        constraints.position_constraints.append(position_constraint)
        constraints.orientation_constraints.append(orientation_constraint)
        request.goal_constraints.append(constraints)

        goal_msg.request = request

        self.get_logger().info(f'Sending goal: position=({x}, {y}, {z})')
        send_goal_future = self._action_client.send_goal_async(
            goal_msg, 
            feedback_callback=self.feedback_callback
        )
        send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().error('Goal rejected')
            return
        self.get_logger().info('Goal accepted')
        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(self.result_callback)

    def result_callback(self, future):
        result = future.result().result
        if result.error_code.val == 1:  # SUCCESS
            self.get_logger().info('Motion completed successfully!')
        else:
            self.get_logger().error(f'Motion failed with error code: {result.error_code.val}')

    def feedback_callback(self, feedback_msg):
        self.get_logger().info(f'State: {feedback_msg.feedback.state}')


def main(args=None):
    rclpy.init(args=args)
    commander = MoveItCommander()

    # Example: move to a pose (adjust coordinates for your setup)
    
    # Position: x=0.3898, y=-0.0290, z=0.4260 | Orientation: x=0.9966, y=-0.0650, z=-0.0483, w=0.0116
    pose_a = dict(x=0.3898, y=-0.0290, z=0.4260, qx=0.9966, qy=-0.0650, qz=-0.0483, qw=0.0116)

    # Position: x=0.3787, y=-0.0338, z=0.3235 | Orientation: x=0.9449, y=0.3190, z=-0.0697, w=-0.0242
    pose_b = dict(x=0.4787, y=-0.2338, z=0.5235, qx=0.9449, qy=0.3190, qz=-0.0697, qw=-0.0242)
    # commander.send_pose_goal(
    #     x=0.3898,
    #     y=-0.0290,
    #     z=0.4260,
    #     qx=0.9966,
    #     qy=-0.0650,
    #     qz=-0.0483,
    #     qw=0.0116
    # )
    pose = pose_a
    commander.send_pose_goal(**pose)

    try:
        rclpy.spin(commander)
    except KeyboardInterrupt:
        pass
    finally:
        commander.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()