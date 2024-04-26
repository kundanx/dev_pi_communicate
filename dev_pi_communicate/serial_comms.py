#! /usr/bin/env python3

import serial
import struct
import time

from dev_pi_communicate.crc8 import crc8
from dev_pi_communicate.joy import packet_to_send__vel
from dev_pi_communicate.camera import packet_to_send_camera
from std_msgs.msg import Float32MultiArray
from std_msgs.msg import Float64MultiArray

START_BYTE= 0xA5
serial_baudrate = 115200
serial_port_address_FTDI='/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A50285BI-if00-port0'
serial_port_address_black='/dev/serial/by-id/usb-1a86_USB2.0-Serial-if00-port0'

# rx_data_size= 26 #38

class serial_comms:
    def __init__(self, serial_port, serial_baudrate, rx_data_size_, tx_data_size_):
        self.serial = serial.Serial(serial_port, serial_baudrate, timeout=1.0)
        self.rx_data_size = rx_data_size_
        self.tx_data_size = tx_data_size_
        self.start_byte_found = False
        self.last_recieve_time = time.time()
        
    def write_data(self,data):
        self.serial.write(data)
        self.serial.reset_output_buffer()
        
    
    def read_data(self):  
        hash_not_matched_count = 0 
        if self.serial.in_waiting < self.rx_data_size:
            return 
        if not self.start_byte_found:
            byte = self.serial.read(1)
            # print(byte)
            if int.from_bytes(byte, 'big') == START_BYTE:
                    self.start_byte_found=True
        else :
            self.start_byte_found = False
            data_str = self.serial.read(self.rx_data_size-1)
            hash = self.calc_crc(data_str)

            if hash == data_str[-1]:
                self.serial.reset_input_buffer()
                # now = time.time()
                # diff_rx = now - self.last_recieve_time
                # print(f"{diff_rx =}")
                self.last_recieve_time = time.time()
                return data_str
            hash_not_matched_count += 1
            print(f"data not matched,count: {hash_not_matched_count}")
            print(data_str)
            return
    
    def close(self):
        self.serial.close()


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

