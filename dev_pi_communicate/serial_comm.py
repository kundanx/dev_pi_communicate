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

class serial_comms:
    def __init__(self, serial_port, serial_baudrate, data_size_):
        self.serial_port = serial.Serial(serial_port, serial_baudrate, timeout=1.0)
        
        self.rx_data_size= data_size_
        self.is_waiting_for_start_byte = True

        # self.start_time = time.time()
        # self.start_time_ns = time.monotonic_ns()

    def write_data(self,data):
        self.serial_port.write(data)
        self.serial_port.reset_output_buffer() 
    
    def read_data(self):   
        print("now")
        if self.serial_port.in_waiting < self.rx_data_size:
            print("then")
            return None
         
        if self.is_waiting_for_start_byte:
            byte = self.serial_port.read(1)
            if int.from_bytes(byte, 'big') == START_BYTE:
                # print(byte)
                self.is_waiting_for_start_byte = False
                print("here11")

            else:
                # pass
                print("Start Byte Not Matched")
        else:
            print("here")
            self.is_waiting_for_start_byte = True
            data_str = self.serial_port.read(self.rx_data_size-1)
            hash = self.calc_crc(data_str[:-1])
            if hash == data_str[-1]:
                self.serial_port.reset_input_buffer()
                return data_str
            else:
                # pass
                print(data_str)
        return None
    
    def close_port(self):
        self.serial_port.close()

    def calc_checksum(self, data=[]):
        for i in range(0,len(data)):
            checksum = checksum ^ data[i]
        return checksum

    def calc_crc(self, data=[]):
        hash_func=crc8()
        hash_func.update(data[0:-1])
        return hash_func.digest()[0]


