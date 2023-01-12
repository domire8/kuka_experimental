from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, FindExecutable, LaunchConfiguration, PathJoinSubstitution

from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    launch_argument = DeclareLaunchArgument(
        "model", description="URDF/XACRO description file with the robot.", default_value="kr16_2"
    )

    robot_description_content = Command(
        [
            PathJoinSubstitution([FindExecutable(name="xacro")]),
            " ",
            PathJoinSubstitution(
                [FindPackageShare("kuka_kr16_support"), "urdf/", LaunchConfiguration("model")]),
            ".xacro"
        ]
    )

    robot_state_pub_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="both",
        parameters=[{"robot_description": robot_description_content}],
    )

    joint_state_pub_node = Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui",
        output="both",
    )

    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        arguments=["-d", PathJoinSubstitution([FindPackageShare("kuka_kr16_support"), "config/kr16.rviz"])],
        output="log",
    )

    nodes = [
        robot_state_pub_node,
        joint_state_pub_node,
        rviz_node,
    ]

    return LaunchDescription([launch_argument] + nodes)