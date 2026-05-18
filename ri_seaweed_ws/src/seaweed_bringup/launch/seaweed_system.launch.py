from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution

from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    realsense_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                FindPackageShare("realsense2_camera"),
                "launch",
                "rs_launch.py",
            ])
        ),
        launch_arguments={
            "pointcloud__neon_.enable": "true", # CHANGE TO "pointcloud.enable": "true" FOR NON ARM SYSTEMS
            "pointcloud__neon_.stream_filter": "1",
            "enable_color": "false",
        }.items(),
    )

    gripper_driver = Node(
        package="gripper",
        executable="gripper_driver",
        name="gripper_driver",
        output="screen",
    )

    detect_objects = Node(
        package="machine_vision",
        executable="detect_objects",
        name="detect_objects",
        output="screen",
    )

    franka_moveit_commander = Node(     #CHANGE TO NON FRANKA MOVEIT COMMANDER WHEN MOVING TO THE KUKA MANIPULATOR
        package="moveit_commander",
        executable="franka_moveit_commander",
        name="franka_moveit_commander",
        output="screen",
    )

    return LaunchDescription([
        realsense_launch,

        gripper_driver,

        TimerAction(
            period=3.0,
            actions=[
                detect_objects,
            ],
        ),

        franka_moveit_commander,
    ])