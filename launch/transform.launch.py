#! /usr/bin/env python3

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_xml.launch_description_sources import XMLLaunchDescriptionSource


from launch.actions import (EmitEvent, ExecuteProcess,
                            LogInfo, RegisterEventHandler, TimerAction)
from launch.conditions import IfCondition
from launch.event_handlers import (OnExecutionComplete, OnProcessExit,
                                OnProcessIO, OnProcessStart, OnShutdown)
from launch.events import Shutdown
from launch.substitutions import (EnvironmentVariable, FindExecutable,
                                 LocalSubstitution, PythonExpression)





def generate_launch_description():
    pkg_path = os.path.join(get_package_share_directory('dev_pi_communicate'))
    
    # Base_link to laser_frame tranformation
    baseLink_laserFrame_tf= Node(
        package='dev_pi_communicate',
        executable='baseLink_laserFrame_tf',
        output= 'screen'
    )
    baseLink_imuLink_tf= Node(
        package='dev_pi_communicate',
        executable='baseLink_imuLink_tf',
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
    map_odom_tf= Node(
        package='dev_pi_communicate',
        executable='map_odom_tf',
        output='screen'
    )

    return LaunchDescription([
        baseLink_laserFrame_tf,

        RegisterEventHandler(
            OnProcessStart(
                target_action=baseLink_laserFrame_tf,

                on_start=[
                    baseLink_imuLink_tf
                ]
            )
        ),


        RegisterEventHandler(
            OnProcessStart(
                target_action=baseLink_imuLink_tf,

                on_start=[
                    odom_baseLink_tf
                ]
            )
        ),


        RegisterEventHandler(
            OnProcessStart(
                target_action=odom_baseLink_tf,

                on_start=[
                    map_odom_tf,
                    # map_baseLink_tf
                ]
            )
        ),


        # baseLink_imuLink_tf,
        # odom_baseLink_tf,
        # # map_baseLink_tf
        # map_odom_tf
    ])