#! /usr/bin/env python3
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_xml.launch_description_sources import XMLLaunchDescriptionSource


def generate_launch_description():

    gamefeild_path = os.path.join(
        get_package_share_directory("my_gamefield"), "launch/rsp.launch.py"
    )
    gamefeild = IncludeLaunchDescription(PythonLaunchDescriptionSource([gamefeild_path]))

    robot_path = os.path.join(
        get_package_share_directory("robot"), "launch/robot.launch.py"
    )
    robot = IncludeLaunchDescription(PythonLaunchDescriptionSource([robot_path]))

    return LaunchDescription(
        [
            gamefeild,
            robot           
        ]
    )