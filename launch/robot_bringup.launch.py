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


    # launch transforms
    tf_path = os.path.join(
        get_package_share_directory("dev_pi_communicate"), "launch/transform.launch.py"
    )
    tf = IncludeLaunchDescription(PythonLaunchDescriptionSource([tf_path]))

    serials_path = os.path.join(
        get_package_share_directory("dev_pi_communicate"), "launch/serials.launch.py"
    )
    serials = IncludeLaunchDescription(PythonLaunchDescriptionSource([serials_path]))

    linefollow_path = os.path.join(
        get_package_share_directory('linefollow'), 'launch/LineFollower.launch.py'
    )
    linefollower = IncludeLaunchDescription(PythonLaunchDescriptionSource([linefollow_path]))

    nav2_path = os.path.join(
        get_package_share_directory('dev_pi_communicate'), 'launch/navigation_launch.py'
    )
    nav2_launch = IncludeLaunchDescription(PythonLaunchDescriptionSource([nav2_path]))

    bt_path = os.path.join(
        get_package_share_directory('behaviour_plugins'), 'launch/bt.launch.py'
    )
    bt_launch = IncludeLaunchDescription(PythonLaunchDescriptionSource([bt_path]))

    landmark_pose_estimation_node = Node(
        package="dev_pi_communicate",
        executable="landmark_pose_estimation_node",
        output="screen",
    )

    dummy_node = ExecuteProcess(
        cmd=
            [
                [
                "sleep 2"
                ]
            ],
        shell=True
    )
    
    return LaunchDescription(
        [
            landmark_pose_estimation_node,
            # serials,
            # dummy_node,
            
            RegisterEventHandler(
            OnProcessStart(
                target_action=landmark_pose_estimation_node,
                on_start=[
                    serials,
                ]
                )
            ),
            
            RegisterEventHandler(
            OnExecutionComplete(
                target_action=serials,
                on_completion=[
                    tf,
                ]
                )
            ),
            RegisterEventHandler(
            OnExecutionComplete(
                target_action=tf,
                on_completion=[
                    linefollower,
                ]
                )
            ),

            # RegisterEventHandler(
            # OnExecutionComplete(
            #     target_action=linefollower,
            #     on_completion=[
            #         nav2_launch,
            #     ]
            #     )
            # ),
            # RegisterEventHandler(
            # OnExecutionComplete(
            #     target_action=nav2_launch,
            #     on_completion=[
            #         bt_launch,
            #     ]
            #     )
            # ),
        ]
    )
