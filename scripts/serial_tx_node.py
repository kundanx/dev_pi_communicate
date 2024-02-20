#! /usr/bin/env python3

# This node subscribes to /cmd_robot_vel topic to recieve velocity commands in serial data packet form 
# and write the data to stm discovery

import rclpy
import struct
import math


from math import sin, cos, radians
from rclpy.node import Node 
from nav_msgs.msg import Odometry
from std_msgs.msg import Float64MultiArray

from dev_pi_communicate.crc8 import crc8
from dev_pi_communicate.serial_comm import serial_comms

START_BYTE= 0b10100101
serial_baudrate = 115200
serial_port_address_FTDI='/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A50285BI-if00-port0'
serial_port_address_black='/dev/serial/by-id/usb-1a86_USB2.0-Serial-if00-port0'
    
class Serial_comms_TX_node(Node):
    
    def __init__(self):

        super().__init__("serial_comm_TX_node")

        self.usb_port2 = serial_comms(serial_port_address_FTDI, serial_baudrate)

        # Subscriber to joystick data
        self.sub_joy = self.create_subscription(
            Float64MultiArray,
            "/cmd_robot_vel", #/cmd_robot_vel
            self.send_joy_data,
            10 )
        
        self.get_logger().info("Transmission ready...")
        
    # Joystick read callback function
    def send_joy_data(self,msg:Float64MultiArray):
        # print("here recieve")
        # print(f"{msg.data[0]=}\n{msg.data[1]=}\n{msg.data[2]=}")
        joy_data=[
            bytes(struct.pack("B",START_BYTE)),
            bytes(struct.pack("d",msg.data[0])),
            bytes(struct.pack("d",msg.data[1])),
            bytes(struct.pack("d",msg.data[2]))
        ]
        joy_data = b''.join(joy_data)
        hash=self.calculate_crc(joy_data)
        joy_data=[joy_data,
            bytes(struct.pack('B', hash)) 
        ]
        joy_data=b''.join(joy_data)
        self.usb_port2.write_data(joy_data)
        
    def calculate_checksum(self , data = []):
        digest = int()
        for i in range(1,len(data)):
            digest += data[i]
        return int(digest)
    
    def calculate_crc(self, data=[]):
        hash_func=crc8()
        hash_func.update(data[1:])
        return hash_func.digest()[0]
    

def main(args=None):
    rclpy.init()
    node = Serial_comms_TX_node()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:  
        pass
    rclpy.shutdown()
   
if __name__ =='__main':
    main()
