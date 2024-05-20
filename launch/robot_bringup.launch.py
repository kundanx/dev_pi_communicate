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
    # ds4_path = os.path.join(get_package_share_directory('ds4_driver'),'launch/ds4_driver.launch.xml')
    # ds4_driver=IncludeLaunchDescription(
    #     XMLLaunchDescriptionSource([ds4_path],)
    # )

    ekf_pkg_path = os.path.join(get_package_share_directory('robot_localization'),'launch/ekf.launch.py')
    ekf_pkg=IncludeLaunchDescription(
        PythonLaunchDescriptionSource([ekf_pkg_path])
    )
    

    # rplidar=Node(
    #     package='rplidar_ros',
    #     executable='rplidar_composition',
    #     parameters=[os.path.join(get_package_share_directory("dev_pi_communicate"), 'config', 'rplidar.yaml')],
    #     output="screen"
    # )

    # laser_filter= Node(
    #     package='laser_filters',
    #     executable='scan_to_scan_filter_chain',
    #     parameters=[os.path.join(get_package_share_directory("dev_pi_communicate"), 'config', 'laser_filter.yaml')],
    #     output='screen'
    
    # )


    # serial bridge node
    serial_bridge= Node(
        package='dev_pi_communicate',
        executable='serial_bridge',
        output='screen'
    )
     # serial bridge node
    serial_bluepill= Node(
        package='dev_pi_communicate',
        executable='serial_bluepill',
        output='screen'
    )
     # serial bridge node
    landmark_pose_estimation_node= Node(
        package='dev_pi_communicate',
        executable='landmark_pose_estimation_node',
        output='screen'
    )

    ds4_uart_node= Node(
        package='dev_pi_communicate',
        executable='ds4_uart_node',
        output='screen'
    )

    ds4_node= Node(
        package='dev_pi_communicate',
        executable='ds4_node',
        output='screen'
    )

    imu_uart_node= Node(
        package='dev_pi_communicate',
        executable='imu_uart_node',
        output='screen'
    )

    cmdVel_to_serialBridge=Node(
        package='dev_pi_communicate',
        executable='cmdVel_to_serialBridge',
        output='screen'
    )

    return LaunchDescription([
        # rplidar,
        # laser_filter,
        # imu_uart_node,
        serial_bridge,
        # serial_bluepill,
        landmark_pose_estimation_node,
        # serial_rx_node,
        # serial_tx_node,
        # ds4_uart_node,
        # ds4_node,
        ekf_pkg,
        # tf,
        cmdVel_to_serialBridge

    ])
