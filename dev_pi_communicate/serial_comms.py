#! /usr/bin/env python3

import serial
import time
import logging

from dev_pi_communicate.crc8 import crc8

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

START_BYTE= 0xA5
class serial_comms:
    def __init__(self, serial_port, serial_baudrate, rx_data_size_, tx_data_size_, hash_func_="CRC"):
        try:
            self.serial = serial.Serial(serial_port, serial_baudrate, timeout=1.0)
        except serial.SerialException as e:
            logger.error(f"[Serial_coms]:Serial port error: {e}")
            self._reopen_serial_port()
            
        self.serial_port = serial_port
        self.serial_baudrate = serial_baudrate
        self.rx_data_size = rx_data_size_
        self.tx_data_size = tx_data_size_
        self.hash_func = hash_func_
        self.hash_not_matched_count = 0
        self.start_byte_found = False
        
    def write_data(self,data):
        self.serial.write(data)
        self.serial.reset_output_buffer()
        
    def read_data(self):  
        if not self.start_byte_found:
            try:
                if self.serial.in_waiting >= 1:
                    byte = self.serial.read(1)
                    if int.from_bytes(byte, 'big') == START_BYTE:
                        self.start_byte_found=True
                    else: 
                        print("[Serial_coms]: Start byte not matched")
                else:
                    # print("[Serial_coms]:timeoutwaiting for start byte")
                    return
            except serial.SerialException as e:
                logger.error(f"[Serial_coms]::Serial port error: {e}")
                self._reopen_serial_port()

        else :
            try:
                if self.serial.in_waiting >= self.rx_data_size-1:
                    self.start_byte_found = False
                    data_str = self.serial.read(self.rx_data_size-1)
                    if self.hash_func == "CRC":
                        hash = self.calc_crc(data_str)
                    elif self.hash_func == "CSUM":
                        hash = self.calc_checksum(data_str)
    
                    if hash == data_str[-1]:
                        # self.serial.reset_input_buffer()
                        self.hash_not_matched_count = 0
                        return data_str
                    self.hash_not_matched_count += 1
                    print(f"[Serial_coms]:hash not matched,count: {self.hash_not_matched_count}")
                    return
                else:
                    # print("[Serial_coms]:timeout waiting for data")
                    return

                
            except serial.SerialException as e:
                logger.error(f"[Serial_coms]:Serial port error: {e}")
                self._reopen_serial_port()
    
    def close(self):
        self.serial.close()
    
    def _reopen_serial_port(self):
        try:
            time.sleep(2)            
            self.serial.close()
            self.serial = serial.Serial(self.serial_port, self.serial_baudrate, timeout=1.0)
            logger.info("[Serial_coms]::Serial port reopened successfully")
        except serial.SerialException as e:
            logger.error(f"[Serial_coms]:Failed to reopen serial port: {e}")
        except Exception as e:
            logger.error(f"[Serial_coms]:Serial port unknown error: {e}")




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

