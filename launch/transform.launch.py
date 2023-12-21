#! /usr/bin/env python3
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    pkg_path = os.path.join(get_package_share_directory('dev_pi_communicate'))
    
    # Base_link to laser_frame tranformation
    baseLink_laserFrame_tf= Node(
        package='dev_pi_communicate',
        executable='baseLink_laserFrame_tf',
        output= 'screen'
    )
    # Odom_Frame to Base_Footprint transformation
    odom_baseLink_tf= Node(
        package='dev_pi_communicate',
        executable='odom_baseLink_tf',
        output='screen'
    )

    map_baseLink_tf= Node(
        package='dev_pi_communicate',
        executable='map_baseLink_tf',
        output='screen'
    )

    return LaunchDescription([
        baseLink_laserFrame_tf,
        odom_baseLink_tf,
        map_baseLink_tf
    ])