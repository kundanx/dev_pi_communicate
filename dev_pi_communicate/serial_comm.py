#! /usr/bin/env python3

import serial
import struct
import time

from dev_pi_communicate.crc8 import crc8
from dev_pi_communicate.joy import packet_to_send__vel
from dev_pi_communicate.camera import packet_to_send_camera
from std_msgs.msg import Float32MultiArray

START_BYTE= 0b10100101
serial_baudrate = 115200
serial_port_address_FTDI='/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A50285BI-if00-port0'
serial_port_address_black='/dev/serial/by-id/usb-1a86_USB2.0-Serial-if00-port0'

class serial_comms:
    def __init__(self, serial_port, serial_baudrate):
        self.serial = serial.Serial(serial_port, serial_baudrate)
        self.start_time = time.time()
        self.start_time_ns = time.monotonic_ns()

        self.data_to_send= START_BYTE
        self.data_to_send= bytes(struct.pack("B", self.data_to_send))

    def write_data(self,data):
        self.serial.write(data)
        # print(data)
        # print("sent")
        self.serial.reset_output_buffer()
        
    
    def read_data(self):   
       
        # if self.serial.in_waiting >= 26:
        while True :
            # print("here")
            start_byte_found = False
            while not start_byte_found:
                byte = self.serial.read(1)
                # print(byte)
                if int.from_bytes(byte, 'big') == START_BYTE:
                    # self.current_time=time.time()
                    # print(f"new data at time {self.current_time - self.start_time }")
                    # print(f"new data recieved at every {time.monotonic_ns() - self.curr_time_ns}")
                    # self.curr_time_ns = time.monotonic_ns()
                    # self.start_time = self.current_time
                    data_str = self.serial.read(25)
                    start_byte_found=True
           
            hash = self.calc_crc(data_str)
            if hash == data_str[-1]:
                self.serial.reset_input_buffer()
                # print("recieved")
                return data_str
            print("data not matched")
            print(data_str)


    def calc_checksum(self, data=[]):
        for i in range(0,len(data)):
            checksum = checksum ^ data[i]
        return checksum

    def calc_crc(self, data=[]):
        hash_func=crc8()
        hash_func.update(data[0:-1])
        return hash_func.digest()[0]
    
    

    def __del__(self):
        self.serial.close()



# class send_data_to_serial_port():
#     def __init__(self):
#         self.usb_port = serial_comms(serial_port_address_black, serial_baudrate)
#         self.sub_joy = self.create_subscription(Float32MultiArray, "/cmd_robot_vel",self.send_joy_data ,10)
    
#     def send_vel(self, vel_x, vel_y, vel_z,ang_x,ang_y,ang_z):
#         vel_data= [
#             bytes(struct.pack("f", vel_x)),
#             bytes(struct.pack("f", vel_y)),
#             bytes(struct.pack("f", vel_z)),
#             bytes(struct.pack("f", ang_x)),
#             bytes(struct.pack("f", ang_y)),
#             bytes(struct.pack("f", ang_z))
#             ]
#         vel_data= b''.join(vel_data)
#         print(vel_data)
#         self.usb_port.write_data(vel_data)
        
#     def send_camera_data(self, data:packet_to_send_camera):
#         camera_data = [
#             bytes(struct.pack("B", data.byte[0])),
#             bytes(struct.pack('f', data.byte[1])),
#             bytes(struct.pack('f', data.byte[2])),
#             bytes(struct.pack('f', data.byte[3]))
#         ]
#         camera_data= b''.join(camera_data)
#         hash= self.calculate_crc(camera_data)
#         camera_data =[camera_data,
#             bytes(struct.pack('B', hash))   
#         ]
#         camera_data= b''.join(camera_data)
#         print("ok")
#         print(camera_data)
#         self.usb_port.write_data(camera_data)   
        
#     def send_joy_data(self,msg:Float32MultiArray):
#         joy_data=[
#             bytes(struct.pack("B",START_BYTE)),
#             bytes(struct.pack("B",msg.data[0])),
#             bytes(struct.pack("B",msg.data[1])),
#             bytes(struct.pack("B",msg.data[2]))
#         ]
#         joy_data = b''.join(joy_data)
#         hash=self.calculate_crc(joy_data)
#         joy_data=[joy_data,
#             bytes(struct.pack('B', hash)) 
#         ]
#         joy_data=b''.join(joy_data)
#         print(joy_data)
#         self.usb_port.write(joy_data)
#         self.usb_port.reset_output_buffer()
 
#     def calculate_checksum(self , data = []):
#         digest = int()
#         for i in range(1,len(data)):
#             digest += data[i]
#         return int(digest)
    
#     def calculate_crc(self, data=[]):
#         hash_func=crc8()
#         hash_func.update(data[1:])
#         return hash_func.digest()[0]
    
#     def read(self):
#         return(self.usb_port.read())
#     def kill(self):
#         self.usb_port.__del__()

# serial_port= send_data_to_serial_port(serial_port_address_black, serial_baudrate)




