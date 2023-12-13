#! /usr/bin/env python3
import struct
START_BYTE_camera= 0b10100101


class base_vel():
    def __init__(self):
        self.vel_x = float()
        self.vel_y = float()
        self.omega = float()

class packet_to_send_camera():
    def __init__(self):
        self.data_to_send_camera = [0]*14
    
    def create_packet(self, commands=base_vel()):
        self.data_to_send_camera[0]= START_BYTE_camera
        self.data_to_send_camera[1]= commands.vel_x
        self.data_to_send_camera[2]= commands.vel_y
        self.data_to_send_camera[3]= commands.omega
        self.data_to_send_camera[4]= self.calculate_checksum(self.data_to_send_camera)
    
    def calculate_checksum(self , data = []*4):
        digest = int()
        for i in range(1,3):
            digest += data[i]
        return int(digest)