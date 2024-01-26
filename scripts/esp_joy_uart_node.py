#! /usr/bin/env python3

# Node which recieves joy data from esp32 serially through gpio 14(TXD) and 15(RXD) and publish to ps4_node

import rclpy
import serial
import struct
import ctypes
import time

from rclpy.node import Node 
from dev_pi_communicate.crc8 import crc8
from sensor_msgs.msg import Joy

START_BYTE= 0b10100101
serial_baudrate = 115200
serial_port_address='/dev/ttyS0'
rx_data_size = 10
d_band = 30

payloadMask =[
    0b00000001, # L1
    0b00000010, # R1
    0b00000100, # Down
    0b00001000, # Up
    0b00010000, # Cricle
    0b00100000, # Cross
    0b01000000, # Triangle
    0b10000000] # Square

class esp_joy_node(Node):
    
    def __init__(self):

        super().__init__("esp_joy_node")

        self.esp_uart = serial.Serial(serial_port_address, serial_baudrate)
        
        #  Odom data publisher
        self.joy_publisher = self.create_publisher(Joy, '/joy', 10)
        self.create_timer(0.03, self.serial_read_callback)
        self.start = time.time()
        self.get_logger().info("Recieving data")
        
    # Read callback function
    def serial_read_callback(self):
        count = 0
        while True:
            # print("here")
            start_byte_found = False
            while not start_byte_found:
                byte = self.esp_uart.read(1)
                # print(byte)
                if int.from_bytes(byte, 'big') == START_BYTE:
                    
                    data_str = self.esp_uart.read(rx_data_size-1)
                    start_byte_found=True
           
            hash = self.calc_crc(data_str)
            if hash != data_str[-1]:
                count += 1
                print(f"data not matched,count: {count}")
                print(data_str)
                
            self.esp_uart.reset_input_buffer()
            # print("Recieved")
            self.process_data(data_str)
    
    def process_data(self,data_):
        joy_msg = Joy()
        joy_msg.header.frame_id="joy_esp"
        joy_msg.header.stamp=self.get_clock().now().to_msg()
        joy_msg.axes = [0.0]*6
        joy_msg.buttons = [0]*14

        buttons_1, buttons_2, LT, RT, LStickY, LStickX, RStickY, RStickX, hash= struct.unpack("BBBBBBBBB", data_[0:])
        
        # converting into signed interger
        LStickX = ctypes.c_int8(LStickX).value
        LStickY = ctypes.c_int8(LStickY).value
        RStickX = ctypes.c_int8(RStickX).value
        RStickY = ctypes.c_int8(RStickY).value

        #  introducing dead band
        if LStickX >= -d_band and LStickX <= d_band:
            LStickX = 0.0
        if LStickY >= -d_band and LStickY <= d_band:
            LStickY = 0.0
        if RStickX >= -d_band and RStickX <= d_band:
            RStickX = 0.0
        if RStickY >= -d_band and RStickY <= d_band:
            RStickY = 0.0
        if  LT <= d_band:
            LT = 0
        if  RT <= d_band:
            RT = 0

        # mapping to -1.0 to 1.0
        joy_msg.axes[0]= self.map_(LStickX, 127, -127, 1.00000000, -1.00000000)
        joy_msg.axes[1]= self.map_(LStickY, -127, 127, 1.00000000, -1.00000000)
        joy_msg.axes[2]= self.map_(RStickX, 127, -127, 1.00000000, -1.00000000)
        joy_msg.axes[3]= self.map_(RStickY, -127, 127, 1.00000000, -1.00000000)
        joy_msg.axes[4]= self.map_(LT, 0, 255, 0.0000000, 1.0000000)
        joy_msg.axes[5]= self.map_(RT,  0, 255, 0.0000000, 1.0000000)
        
        # Parse buttons
        if buttons_1 & payloadMask[5]:
            joy_msg.buttons[0] = 1
        if buttons_1 & payloadMask[4]:
            joy_msg.buttons[1] = 1
        if buttons_1 & payloadMask[6]:
            joy_msg.buttons[2] = 1
        if buttons_1 & payloadMask[7]:
            joy_msg.buttons[3] = 1
        if buttons_1 & payloadMask[2]:
            joy_msg.buttons[4] = 1
        if buttons_2 & payloadMask[3]:
            joy_msg.buttons[5] = 1
        if buttons_1 & payloadMask[3]:
            joy_msg.buttons[6] = 1
        if buttons_2 & payloadMask[4]:
            joy_msg.buttons[7] = 1
        
        if buttons_1 & payloadMask[0]:
            joy_msg.buttons[8] = 1
        if buttons_1 & payloadMask[1]:
            joy_msg.buttons[9] = 1
        if buttons_2 & payloadMask[0]:
            joy_msg.buttons[10] = 1
        if buttons_2 & payloadMask[1]:
            joy_msg.buttons[11] = 1
        if buttons_2 & payloadMask[7]:
            joy_msg.buttons[12] = 1
        if buttons_2 & payloadMask[5]:
            joy_msg.buttons[13] = 1
        # if buttons_2 & payloadMask[4]:
        #     joy_msg.buttons[14] = 1
        # if buttons_2 & payloadMask[4]:
        #     joy_msg.buttons[15] = 1

        # publish joy_msg
        self.joy_publisher.publish(joy_msg)

    def calc_checksum(self, data=[]):
        for i in range(0,len(data)):
            checksum = checksum ^ data[i]
        return checksum

    def calc_crc(self, data=[]):
        hash_func=crc8()
        hash_func.update(data[0:-1])
        return hash_func.digest()[0]
    
    def map_(self, x:int,  in_min:int,  in_max:int,out_min:float, out_max:float):
        run = in_max - in_min
        rise = out_max - out_min
        delta = x - in_min
        return (delta * rise) / run + out_min

def main(args=None):
    rclpy.init()
    serial_node = esp_joy_node()
    try:
        rclpy.spin(serial_node)
    except KeyboardInterrupt:  
        pass
    rclpy.shutdown()
   
if __name__ =='__main':
    main()

