#! /usr/bin/env python3
import struct
from dev_pi_communicate.crc8 import crc8

START_BYTE_camera= 0b10100101

class base_vel():
    def __init__(self):
        self.vel_x = float()
        self.vel_y = float()
        self.omega = float()

class packet_to_send_camera():
    def __init__(self):
        self.byte = [0]*4
    
    def create_packet(self, commands=base_vel()):
        self.byte[0]=START_BYTE_camera
        self.byte[1]= commands.vel_x
        self.byte[2]= commands.vel_y
        self.byte[3]= commands.omega
        print(self.byte)
    
