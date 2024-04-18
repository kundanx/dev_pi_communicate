#! /usr/bin/env python3

# This node subscribes to /cmd_robot_vel topic to recieve velocity commands in serial data packet form 
# and write the data to stm discovery

import rclpy
import struct
import sys
import math
import ctypes


from math import sin, cos, radians
from rclpy.node import Node 
from nav_msgs.msg import Odometry
from std_msgs.msg import Float32MultiArray
from std_msgs.msg import Float64MultiArray
from std_msgs.msg import UInt8

from dev_pi_communicate.crc8 import crc8
from dev_pi_communicate.serial_comm import serial_comms

START_BYTE= 0b10100101

PID_cmd_vel = 0x01
PID_act_vel = 0X02

serial_baudrate = 115200
serial_port_address_FTDI='/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A50285BI-if00-port0'
serial_port_address_black='/dev/serial/by-id/usb-1a86_USB2.0-Serial-if00-port0'

class Actuator:
    def __init__(self, isOn, pwm ):
        self.isOn : int = isOn
        self.pwm : float = pwm

PacketLength_cmd_vel = 0xc
PacketLength_act_vel = 0x5
    
class Serial_comms_TX_node(Node):
    
    def __init__(self):

        super().__init__("serial_comm_TX_node")
        self.count : float = 0.0
        self.usb_port2 = serial_comms(serial_port_address_FTDI, serial_baudrate)
        self.intake_roller = Actuator(1, 0.5)
        self.isCmdVelSending : bool = True
        self.isActuatorVelSending : bool = False

        # Subscriber to joystick data
        self.sub_joy = self.create_subscription(
            Float32MultiArray,
            "/cmd_robot_vel", #/cmd_robot_vel
            self.send_cmd_vel_data,
            10 )

        self.create_timer(0.05, self.send_actuator_vel_data)
        self.get_logger().info("Transmission ready...")

    def subs_callback_2(self, msg:UInt8):
        self.motor_switch = msg

        
    # Joystick read callback function
    def send_cmd_vel_data(self,msg):
        if not self.isActuatorVelSending:
            self.isCmdVelSending = True
            cmd_vel_data=[
                bytes(struct.pack("B",START_BYTE)),
                bytes(struct.pack("B",PID_cmd_vel)),
                bytes(struct.pack("B",PacketLength_cmd_vel))
            ]
            cmd_vel_data = b''.join(cmd_vel_data)
            PID_hash=self.calculate_crc(cmd_vel_data)
            cmd_vel_data=[
                cmd_vel_data,
                bytes(struct.pack('B', PID_hash)) 
            ]
            cmd_vel_data = b''.join(cmd_vel_data)
            cmd_vel_data=[
                cmd_vel_data,
                bytes(struct.pack("f",float(msg.data[0]))),
                bytes(struct.pack("f",float(msg.data[1]))),
                bytes(struct.pack("f",float(msg.data[2]))),
            ]
            cmd_vel_data = b''.join(cmd_vel_data)
            data_hash=self.calculate_crc(cmd_vel_data[3:])
            cmd_vel_data=[
                cmd_vel_data,
                bytes(struct.pack('B', data_hash)) 
            ]
            cmd_vel_data=b''.join(cmd_vel_data)
            self.usb_port2.write_data(cmd_vel_data)

            print("*******CMD_VEL********")
            print("PID: %x, length: %x, PID_hash: %x, data_hash: %x " %(cmd_vel_data[1],cmd_vel_data[2],cmd_vel_data[3],cmd_vel_data[-1]))
            # print(cmd_vel_data)
            # print(", size of whole packet: %i" %(cmd_vel_data[-1], cmd_vel_data.__sizeof__()))
            self.isCmdVelSending = False


    def send_actuator_vel_data(self):
        if not self.isCmdVelSending:
            self.isActuatorVelSending = True
            actuator_vel_data=[
                bytes(struct.pack("B",START_BYTE)),
                bytes(struct.pack("B",PID_act_vel)),
                bytes(struct.pack("B",PacketLength_act_vel))
            ]
            actuator_vel_data = b''.join(actuator_vel_data)
            PID_hash=self.calculate_crc(actuator_vel_data)
            actuator_vel_data=[
                actuator_vel_data,
                bytes(struct.pack('B', PID_hash)) 
            ]
            actuator_vel_data = b''.join(actuator_vel_data)
            actuator_vel_data=[
                actuator_vel_data,
                bytes(struct.pack("B",self.intake_roller.isOn)),
                bytes(struct.pack("f",self.intake_roller.pwm)),   

            ]
            actuator_vel_data = b''.join(actuator_vel_data)
            data_hash=self.calculate_crc(actuator_vel_data[3:])
            actuator_vel_data=[
                actuator_vel_data,
                bytes(struct.pack('B', data_hash)) 
            ]
            actuator_vel_data=b''.join(actuator_vel_data)
            self.usb_port2.write_data(actuator_vel_data)

            print("#####ACTUATOR#######")
            # print(actuator_vel_data)
            print("PID: %x, length: %x, PID_hash: %x , data_hash: %x"%(actuator_vel_data[1],actuator_vel_data[2],actuator_vel_data[3],actuator_vel_data[-1]))
            # print("data_hash: %x, size of whole packet: %i, size of struct:%i "%(actuator_vel_data[-1], actuator_vel_data.__sizeof__(), self.intake_roller.__sizeof__()))
            self.isActuatorVelSending = False



        
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
