#! /usr/bin/env python3

import serial
import struct
from dev_pi_communicate.joy import packet_to_send

START_BYTE_JOY= 0b10100101

class serial_comms:
    def __init__(self, serial_port, serial_baudrate):
        self.serial = serial.Serial(serial_port, serial_baudrate)
        self.data_to_send = START_BYTE_JOY

    def merge_all_data(self,data_to_merge):

        self.data_to_send = [self.data_to_send,
                             data_to_merge
                             ]
        self.data_to_send = b''.join(self.data_to_send)


    def write_data(self):
        self.serial.write(self.data_to_send)

    def __del__(self):
        self.serial.close()



class send_data_to_serial_port():
    def __init__(self,serial_port, serial_baudrate):
        self.usb_port = serial_comms(serial_port, serial_baudrate)
    
    
    def send_vel(self, vel_x, vel_y, vel_z,ang_x,ang_y,ang_z):
        vel_data= [
            bytes(struct.pack("f", vel_x)),
            bytes(struct.pack("f", vel_y)),
            bytes(struct.pack("f", vel_z)),
            bytes(struct.pack("f", ang_x)),
            bytes(struct.pack("f", ang_y)),
            bytes(struct.pack("f", ang_z))
            ]
        self.usb_port.merge_all_data(vel_data)
    
    def send_camera_data(self, camera_data):
        camera_data_to_send = [
            bytes(struct.pack('f', camera_data))
        ]
        self.usb_port.merge_all_data(camera_data)
        
    def send_joy_data(self, data= packet_to_send()):
        joy_data=[
            bytes(struct.pack("B",data.byte[0])),
            bytes(struct.pack("B",data.byte[1])),
            bytes(struct.pack("B",data.byte[2])),
            bytes(struct.pack("B",data.byte[3])),
            bytes(struct.pack("B",data.byte[4])),
            bytes(struct.pack("b",data.byte[5])),
            bytes(struct.pack("b",data.byte[6])),
            bytes(struct.pack("b",data.byte[7])),
            bytes(struct.pack("b",data.byte[8])),
            bytes(struct.pack("B",data.byte[9]))
        ]
        self.usb_port.merge_all_data(joy_data)




