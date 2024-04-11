#! /usr/bin/env python3

import serial
import struct
import time

from dev_pi_communicate.crc8 import crc8
from dev_pi_communicate.joy import packet_to_send__vel
from dev_pi_communicate.camera import packet_to_send_camera
from std_msgs.msg import Float32MultiArray
from std_msgs.msg import Float64MultiArray

START_BYTE= 0b10100101
serial_baudrate = 115200
serial_port_address_FTDI='/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A50285BI-if00-port0'
serial_port_address_black='/dev/serial/by-id/usb-1a86_USB2.0-Serial-if00-port0'

rx_data_size= 38

class serial_comms:
    def __init__(self, serial_port, serial_baudrate):
        self.serial = serial.Serial(serial_port, serial_baudrate, timeout=1.0)
        self.start_time = time.time()
        self.start_time_ns = time.monotonic_ns()

        self.data_to_send= START_BYTE
        self.data_to_send= bytes(struct.pack("B", self.data_to_send))

    def write_data(self,data):
        self.serial.write(data)
        print(data)
        # print("sent")
        self.serial.reset_output_buffer()
        
    
    def read_data(self):   
       
        # if self.serial.in_waiting >= 26:
        count = 0
        while True:
            # print("here")
            start_byte_found = False
            while not start_byte_found:
                byte = self.serial.read(1)
                # print(byte)
                if int.from_bytes(byte, 'big') == START_BYTE:
                    
                    data_str = self.serial.read(rx_data_size-1)
                    start_byte_found=True
           
            hash = self.calc_crc(data_str)
            if hash == data_str[-1]:
                
                self.serial.reset_input_buffer()
                # print(data_str)
                # print("recieved")
                return data_str
            count += 1
            print(f"data not matched,count: {count}")
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

