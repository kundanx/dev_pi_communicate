#! /usr/bin/env python3

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch.launch_description_sources import PythonLaunchDescriptionSource


import os

def generate_launch_description():

    # launch transforms
    tf_path = os.path.join(get_package_share_directory('dev_pi_communicate'),'launch','transform.launch.py')
    tf=IncludeLaunchDescription(
        PythonLaunchDescriptionSource([tf_path])
    )

    # joy_node from joy package to interface joystick_contr
    joystick_controller=Node(
        package='joy',
        executable='joy_node',
        output='screen'
    )

    # serial comms to read from STM32 
    serial_comms_node= Node(
        package='dev_pi_communicate',
        executable='serial_comm_node',
        output='screen'
    )

    # interface camera
    camera_node= Node(
        package='dev_pi_communicate',
        executable='camera_node',
        output='screen'
    )

    #control robot using joy stick
    joy_node= Node(
        package='dev_pi_communicate',
        executable='joy_node',
        output='screen'
    )

    # control robot using teleop_twist_key
    teleop_key_node= Node(
        package='dev_pi_communicate',
        executable='teleop_key_node',
        output='screen'
    )

    # run the node
    return LaunchDescription([
        joystick_controller,
        # serial_comms_node,
        # camera_node,
        # teleop_key_node,
        joy_node,
        tf
    ])
