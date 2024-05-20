#! /usr/bin/env python3

# -------------------------SERIAL BRIDGE BETWEEN RASP PI AND STM32-------------------------------
# This node subscribes to
#   I) 'cmd_robot'_vel topic to recieve velocity commands 
#   II) 'act_vel' from BT to recieve actuator control signals, and  write the data to stm discovery

# This node reads odometry value from bluepill and publish the data on
#   I) 'freewheel/odom' topic to ekf filter package through
#   II)'Ball_status' topic to BT

import rclpy
import struct
import message_filters
import time
import math

from math import sin, cos
from rclpy.node import Node 
from std_msgs.msg import UInt8
from nav_msgs.msg import Odometry
from std_msgs.msg import Float32MultiArray
from std_msgs.msg import UInt8MultiArray

from dev_pi_communicate.crc8 import crc8
from dev_pi_communicate.serial_comms import serial_comms

START_BYTE= 0b10100101
RECIEVE_SIZE = 3
TRANSMIT_SIZE = 0
serial_baudrate = 115200
serial_port_address_pi = '/dev/serial0'
serial_port_address_FTDI='/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A50285BI-if00-port0'
serial_port_address_black='/dev/serial/by-id/usb-1a86_USB2.0-Serial-if00-port0'
serial_port_bluepill ='/dev/serial/by-id/usb-STMicroelectronics_STM32_Virtual_ComPort_00517C4B4D34-if00'
    
class tfmini_uart(Node):
    
    def __init__(self):

        super().__init__("TF_MINI_UART")
        self.serial_port = serial_comms(serial_port_address_pi, serial_baudrate, RECIEVE_SIZE, TRANSMIT_SIZE,"CRC")
        
        self.tfmini_distance = self.create_publisher(UInt8, 'tfmini_distance', 10)
        self.timer = self.create_timer(0.03, self.serial_read_callback)
        self.distance = UInt8()

        self.get_logger().info("TF_MINI Uart ready...")
    
    def serial_read_callback(self):
            _data = self.serial_port.read_data()
            if _data == None:
                return

            data_ = struct.unpack("c", _data[0:1])[0]
            print(f"{data_ = }")
        
        #    print(f"{self.ball_stat.data =}")
            self.tfmini_distance.publish(self.distance)
    
def main(args=None):
    rclpy.init()
    node = tfmini_uart()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt: 
        node.serial_port.close()
        node.destroy_node()
        rclpy.try_shutdown()
        exit()

if __name__ =='__main':
    main()
