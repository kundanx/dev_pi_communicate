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
    # launch transforms
    serials_path = os.path.join(
        get_package_share_directory("dev_pi_communicate"), "launch/serials.launch.py"
    )
    serials = IncludeLaunchDescription(PythonLaunchDescriptionSource([serials_path]))

    # ekf_pkg_path = os.path.join(get_package_share_directory('robot_localization'),'launch/ekf.launch.py')
    # ekf_pkg=IncludeLaunchDescription(
    #     PythonLaunchDescriptionSource([ekf_pkg_path])
    # )

    # serial bridge node
    landmark_pose_estimation_node = Node(
        package="dev_pi_communicate",
        executable="landmark_pose_estimation_node",
        output="screen",
    )

    cmdVel_to_serialBridge = Node(
        package="dev_pi_communicate",
        executable="cmdVel_to_serialBridge",
        output="screen",
    )
    rqt_graph = Node(
        package="rqt_graph",
        executable="rqt_graph",
        output="screen",
    )
    return LaunchDescription(
        [
            # serials,
            # ekf_pkg,
            # tf,    
            landmark_pose_estimation_node,    
            # RegisterEventHandler(
            #     OnProcessStart(
            #         target_action=landmark_pose_estimation_node,
            #         on_start=[
            #             cmdVel_to_serialBridge,
            #         ]
            #     )
            # ),
            RegisterEventHandler(
            OnProcessStart(
                target_action=landmark_pose_estimation_node,
                on_start=[
                    tf,
                ]
            )
            ),
        ]
    )
