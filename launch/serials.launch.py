# #! /usr/bin/env python3


# from launch import LaunchDescription
# from launch_ros.actions import Node

# # from dev_pi_communicate.scripts import ir_bluepill_serial


# def generate_launch_description():
#     # serial bridge node
#     serial_bridge = Node(
#         package="dev_pi_communicate", executable="serial_bridge", output="screen"
#     )

#     panasonic_serial = Node(
#         package="dev_pi_communicate", executable="panasonic_serial", output="screen"
#     )

#     ir_bluepill_serial = Node(
#         package="dev_pi_communicate", executable="ir_bluepill_serial", output="screen"
#     )

#     cmdVel_to_serialBridge = Node(
#         package="dev_pi_communicate",
#         executable="cmdVel_to_serialBridge",
#         output="screen",
#     )

#     return LaunchDescription(
#         [serial_bridge, panasonic_serial, ir_bluepill_serial, cmdVel_to_serialBridge]
#     )


#! /usr/bin/env python3

from launch_ros.actions import Node

from launch import LaunchDescription
from launch.actions import (DeclareLaunchArgument, EmitEvent, ExecuteProcess,
                            LogInfo, RegisterEventHandler, TimerAction)
from launch.conditions import IfCondition
from launch.event_handlers import (OnExecutionComplete, OnProcessExit,
                                OnProcessIO, OnProcessStart, OnShutdown)
from launch.events import Shutdown
from launch.substitutions import (EnvironmentVariable, FindExecutable,
                                LaunchConfiguration, LocalSubstitution,
                                PythonExpression)

# from dev_pi_communicate.scripts import ir_bluepill_serial

def generate_launch_description():
    # serial bridge node
    serial_bridge = Node(
        package="dev_pi_communicate", executable="serial_bridge", output="screen"
    )

    panasonic_serial = Node(
        package="dev_pi_communicate", executable="panasonic_serial", output="screen"
    )

    ir_bluepill_serial = Node(
        package="dev_pi_communicate", executable="ir_bluepill_serial", output="screen"
    )

    tfmini_serial = Node(
        package="linefollow", executable="tfmini_serial_node", output="screen"
    )
    cmdVel_to_serialBridge = Node(
        package="dev_pi_communicate",
        executable="cmdVel_to_serialBridge",
        output="screen",
    )

    return LaunchDescription(
#        [serial_bridge, panasonic_serial, ir_bluepill_serial, cmdVel_to_serialBridge]
        [
            serial_bridge,

            RegisterEventHandler(
                OnProcessStart (
                    target_action=serial_bridge,
                    on_start=[
                        panasonic_serial,
                    ]    
                )
            ),

            RegisterEventHandler(
                OnProcessStart(
                    target_action=panasonic_serial,
                    on_start=[
                        ir_bluepill_serial,
                    ]
                )
            ),

            RegisterEventHandler(
                OnProcessStart(
                    target_action=ir_bluepill_serial,
                    on_start=[
                        cmdVel_to_serialBridge,
                    ]
                )
            ),
            RegisterEventHandler(
                OnProcessStart(
                    target_action=cmdVel_to_serialBridge,
                    on_start=[
                        tfmini_serial,
                    ]
                )
            ),
        ]
    )