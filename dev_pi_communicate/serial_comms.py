#! /usr/bin/env python3

import serial
from dev_pi_communicate.crc8 import crc8

START_BYTE= 0xA5
class serial_comms:
    def __init__(self, serial_port, serial_baudrate, rx_data_size_, tx_data_size_, hash_func_="CRC"):
        self.serial = serial.Serial(serial_port, serial_baudrate, timeout=1.0)
        self.rx_data_size = rx_data_size_
        self.tx_data_size = tx_data_size_
        self.hash_func = hash_func_
        self.hash_not_matched_count = 0
        self.start_byte_found = False
        
    def write_data(self,data):
        self.serial.write(data)
        self.serial.reset_output_buffer()
        
    
    def read_data(self):  
        if self.serial.in_waiting < self.rx_data_size:
            return 
        if not self.start_byte_found:
            byte = self.serial.read(1)
            if int.from_bytes(byte, 'big') == START_BYTE:
                    self.start_byte_found=True
        else :
            self.start_byte_found = False
            data_str = self.serial.read(self.rx_data_size-1)
            if self.hash_func == "CRC":
                hash = self.calc_crc(data_str)
            elif self.hash_func == "CSUM":
                hash = self.calc_checksum(data_str)

            if hash == data_str[-1]:
                self.serial.reset_input_buffer()
                self.hash_not_matched_count = 0
                return data_str
            self.hash_not_matched_count += 1
            print(f"data not matched,count: {self.hash_not_matched_count}")
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

