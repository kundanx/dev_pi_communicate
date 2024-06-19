#! /usr/bin/env python3


from launch import LaunchDescription
from launch_ros.actions import Node

from dev_pi_communicate.scripts import ir_bluepill_serial


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

    return LaunchDescription([serial_bridge, panasonic_serial, ir_bluepill_serial])
