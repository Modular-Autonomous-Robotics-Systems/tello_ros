import os

from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import Node

from launch import LaunchDescription
from launch.actions import ExecuteProcess


def generate_launch_description():

    ns = "drone1"

    world_path = os.path.join(
        get_package_share_directory("tello_gazebo"), "worlds", "simple.world"
    )

    urdf_path = os.path.join(
        get_package_share_directory("tello_description"), "urdf", "tello_1.urdf"
    )

    return LaunchDescription(
        [
            ExecuteProcess(
                cmd=[
                    "gazebo",
                    "--verbose",
                    "-s",
                    "libgazebo_ros_init.so",
                    "-s",
                    "libgazebo_ros_factory.so",
                    world_path,
                ],
                output="screen",
            ),
            Node(
                package="tello_gazebo",
                executable="inject_entity.py",
                output="screen",
                arguments=[urdf_path, "0", "0", "1", "0"],
            ),
            Node(
                package="robot_state_publisher",
                executable="robot_state_publisher",
                output="screen",
                arguments=[urdf_path],
            ),
            Node(package="joy", executable="joy_node", namespace=ns, output="screen"),
            Node(
                package="tello_driver",
                executable="tello_joy_main",
                namespace=ns,
                output="screen",
            ),
        ]
    )
