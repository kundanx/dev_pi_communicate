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
serial_port_address_FTDI='/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A50285BI-if00-port0'
serial_port_address_black='/dev/serial/by-id/usb-1a86_USB2.0-Serial-if00-port0'
serial_port_bluepill ='/dev/serial/by-id/usb-STMicroelectronics_STM32_Virtual_ComPort_00517C4B4D34-if00'
    
class Serial_bluepill_comms(Node):
    
    def __init__(self):

        super().__init__("serial_bluepill")
        self.serial_port = serial_comms(serial_port_bluepill, serial_baudrate, RECIEVE_SIZE, TRANSMIT_SIZE,"CRC")
        
        self.ballStatus = self.create_publisher(UInt8, 'Ball_status', 10)
        self.timer1 = self.create_timer(0.025, self.serial_read_callback)
        self.ball_stat = UInt8()

        self.get_logger().info("Serial bluepill ready...")
    
    def serial_read_callback(self):
            _data = self.serial_port.read_data()
            if _data == None:
                return

            data_ = struct.unpack("c", _data[0:1])[0]
            print(f"{data_ = }")
            if data_ == b"R":
                self.ball_stat.data = 1
            elif data_ == b"B":
                self.ball_stat.data = 2
            elif data_ == b'P':
                self.ball_stat.data = 3
            else :  
               self.ball_stat.data = 0
            print(f"{self.ball_stat.data =}")
            self.ballStatus.publish(self.ball_stat)
           
    def calculate_checksum(self , data = []):
        digest = int()
        for i in range(1,len(data)):
            digest += data[i]
        return int(digest)
    
    def calculate_crc(self, data=[]):
        hash_func=crc8()
        hash_func.update(data)
        return hash_func.digest()[0]
    
def main(args=None):
    rclpy.init()
    node = Serial_bluepill_comms()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt: 
        node.serial_port.close()
        node.destroy_node()
        rclpy.try_shutdown()
        exit()

if __name__ =='__main':
    main()
