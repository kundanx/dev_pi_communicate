#! /usr/bin/env python3

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_xml.launch_description_sources import XMLLaunchDescriptionSource


import os

def generate_launch_description():

    # launch transforms
    tf_path = os.path.join(get_package_share_directory('dev_pi_communicate'),'launch/transform.launch.py')
    tf=IncludeLaunchDescription(
        PythonLaunchDescriptionSource([tf_path])
    )

    # ds4_node from ds4_driver package to interface joystick contro
    ds4_path = os.path.join(get_package_share_directory('ds4_driver'),'launch/ds4_driver.launch.xml')
    ds4_driver=IncludeLaunchDescription(
        XMLLaunchDescriptionSource([ds4_path],)
    )

    laser_filter= Node(
        package='laser_filters',
        executable='scan_to_scan_filter_chain',
        parameters=[
            PathJoinSubstitution([
                get_package_share_directory("dev_pi_communicate"),
                "config", "laser_filter.config",
            ]),
        ]
    )


    # serial comms to read from bluepill
    serial_rx_node= Node(
        package='dev_pi_communicate',
        executable='serial_rx_node',
        output='screen'
    )

    # serial comms to write to STM32 
    serial_tx_node= Node(
        package='dev_pi_communicate',
        executable='serial_tx_node',
        output='screen'
    )

    esp_joy_node= Node(
        package='dev_pi_communicate',
        executable='esp_joy_uart_node',
        output='screen'
    )

    ps4_node= Node(
        package='dev_pi_communicate',
        executable='ps4_node',
        output='screen'
    )

    pico_imu_node= Node(
        package='dev_pi_communicate',
        executable='pico_imu_uart_node',
        output='screen'
    )

    nav2_cmd_vel_node=Node(
        package='dev_pi_communicate',
        executable='nav2_cmd_vel',
        output='screen'
    )

    camera_node= Node(
        package='dev_pi_communicate',
        executable='camera_node',
        output='screen'
    )


    return LaunchDescription([
        
        pico_imu_node,
        esp_joy_node,
        ps4_node,
        tf,
        # laser_filter
        # nav2_cmd_vel_node,
        # serial_comms_node
        # camera_node,
    ])
