#! /usr/bin/env python3

import serial
import struct

from dev_pi_communicate.crc8 import crc8
from dev_pi_communicate.joy import packet_to_send_joy
from dev_pi_communicate.camera import packet_to_send_camera

START_BYTE= 0b10100101
serial_baudrate = 115200
serial_port_address='/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A50285BI-if00-port0'

class serial_comms:
    def __init__(self, serial_port, serial_baudrate):
        self.serial = serial.Serial(serial_port, serial_baudrate)

        self.data_to_send= START_BYTE
        self.data_to_send= bytes(struct.pack("B", self.data_to_send))

    def write_data(self,data):
        self.serial.write(data)
        
    
    def read(self):
        while True:
            start_byte_found = False
            while not start_byte_found:
                byte = self.serial.read(1)
                if byte == START_BYTE:
                    data_str = self.serial.read(9)
                    start_byte_found=True
                    print(data_str)
          
            hash = self.calc_crc(data_str)
            if hash == data_str[-1]:
                return data_str
            print("data not matched")

    def calc_checksum(self, data=[]):
        for i in range(0,len(data)):
            checksum = checksum ^ data[i]
        return checksum

    def calc_crc(self, data=[]*9):
        hash_func=crc8()
        hash_func.update(data[0:-1])
        return hash_func.digest()[0]

    def __del__(self):
        self.serial.close()



class send_data_to_serial_port():
    def __init__(self,serial_port_, serial_baudrate_):
        self.usb_port = serial_comms(serial_port_, serial_baudrate_)
    
    
    def send_vel(self, vel_x, vel_y, vel_z,ang_x,ang_y,ang_z):
        vel_data= [
            bytes(struct.pack("f", vel_x)),
            bytes(struct.pack("f", vel_y)),
            bytes(struct.pack("f", vel_z)),
            bytes(struct.pack("f", ang_x)),
            bytes(struct.pack("f", ang_y)),
            bytes(struct.pack("f", ang_z))
            ]
        vel_data= b''.join(vel_data)
        print(vel_data)
        self.usb_port.write_data(vel_data)
        
    def send_camera_data(self, data= packet_to_send_camera()):
        camera_data = [
            bytes(struct.pack("B", data.byte[0])),
            bytes(struct.pack('f', data.byte[1])),
            bytes(struct.pack('f', data.byte[2])),
            bytes(struct.pack('f', data.byte[3]))
        ]
        camera_data= b''.join(camera_data)
        hash= self.calculate_crc(camera_data)
        camera_data =[camera_data,
            bytes(struct.pack('B', hash))   
        ]
        camera_data= b''.join(camera_data)
        print(camera_data)
        self.usb_port.write_data(camera_data)   
        
    def send_joy_data(self, data= packet_to_send_joy()):
        joy_data=[
            bytes(struct.pack("B",data.byte[0])),
            bytes(struct.pack("B",data.byte[1])),
            bytes(struct.pack("B",data.byte[2])),
            bytes(struct.pack("B",data.byte[3])),
            bytes(struct.pack("B",data.byte[4])),
            bytes(struct.pack("b",data.byte[5])),
            bytes(struct.pack("b",data.byte[6])),
            bytes(struct.pack("b",data.byte[7])),
            bytes(struct.pack("b",data.byte[8]))
        ]
        joy_data=b''.join(joy_data)
        hash=self.calculate_crc(joy_data)
        joy_data=[joy_data,
                  hash
        ]
        joy_data=b''.join(joy_data)
        self.usb_port.write_data(joy_data)


    
    def calculate_checksum(self , data = []):
        digest = int()
        for i in range(1,len(data)):
            digest += data[i]
        return int(digest)
    
    def calculate_crc(self, data=[]):
        hash_func=crc8()
        hash_func.update(data[1:])
        return hash_func.digest()[0]

serial_port= send_data_to_serial_port(serial_port_address, serial_baudrate)




