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

    # joy_node from joy package to interface joystick_contr
    param_file= os.path.join(get_package_share_directory('dev_pi_communicate'),'parameter_files','joy-params.yaml')
    joy_node=Node(
        package='joy',
        executable='joy_node',
        output='screen'
        # parameters=[ "deadzone: 0.5",
        #     "autorepeat_rate: 50",
        #     "sticky_buttons: false",
        #     "coalesce_interval_ms: 20"
        #     ]
    )

    # ds4_node from ds4_driver package to interface joystick contro
    ds4_path = os.path.join(get_package_share_directory('ds4_driver'),'launch/ds4_driver.launch.xml')
    ds4_driver=IncludeLaunchDescription(
        XMLLaunchDescriptionSource([ds4_path],)
    )


    # serial comms to read from STM32 
    serial_comms_node= Node(
        package='dev_pi_communicate',
        executable='serial_comm_node',
        output='screen'
    )



    # control robot using PS4
    ps4_node= Node(
        package='dev_pi_communicate',
        executable='ps4_node',
        output='screen'
    )

    # interface camera
    camera_node= Node(
        package='dev_pi_communicate',
        executable='camera_node',
        output='screen'
    )

    micro_ros = Node(
        package= 'micro_ros_agent',
        executable='micro_ros_agent',
        output= 'screen',
        parameters=[
            {'transport':'serial'},
            {'dev':'/dev/serial/by-id/usb-Silicon_Labs_CP2102_USB_to_UART_Bridge_Controller_0001-if00-port0'}     
        ]
    )
    # run the node
    return LaunchDescription([
        # joy_node,
        # ds4_driver,
        # micro_ros,
        ps4_node,
        tf,
        serial_comms_node
        # camera_node,
    ])
