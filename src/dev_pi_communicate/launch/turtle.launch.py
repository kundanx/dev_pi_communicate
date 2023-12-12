#!/bin/env python3

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch.launch_description_sources import PythonLaunchDescriptionSource

import xacro

import math
import os

def generate_launch_description():
    pkg_path = os.path.join(get_package_share_directory('dev_pi_communicate'))

    params={
        "usb_serial_port": "/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A50285BI-if00-port0"
    }
    camera_node= Node(
        package='dev_pi_communicate',
        executable='camera.py',
        output='screen'
    )

    return LaunchDescription([
        camera_node
    ])
