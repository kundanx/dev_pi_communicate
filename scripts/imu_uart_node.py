#! /usr/bin/env python3

# This node recieves imu data from pico serially and publishes to ekf filter package

import rclpy
import serial
import struct
import ctypes
import time
import numpy as np

from rclpy.node import Node 
from dev_pi_communicate.crc8 import crc8

from sensor_msgs.msg import Imu

START_BYTE= 0b10100101
serial_baudrate = 115200
pico_address='/dev/serial/by-id/usb-Raspberry_Pi_Pico_E6611CB71F34112A-if00'
esp_address='/dev/serial/by-id/usb-Silicon_Labs_CP2102_USB_to_UART_Bridge_Controller_0001-if00-port0'
rx_data_size = 82

class pico_imu_node(Node):
    
    def __init__(self):

        super().__init__("imu_uart_node")

        self.pico_usb = serial.Serial(esp_address, serial_baudrate, timeout=1.0)
        
        #  Odom data publisher
        self.imu_publisher = self.create_publisher(Imu, 'imu/data', 10)
        self.create_timer(0.05, self.serial_read_callback)
        self.start = time.time()
        self.get_logger().info("Recieving imu data ..")
        
    # Read callback function
    def serial_read_callback(self):
        # print("here")
        count = 0
        while True:
            start_byte_found = False
            while not start_byte_found:
                byte = self.pico_usb.read(1)
                # self.get_logger().info(byte)
                if int.from_bytes(byte, 'big') == START_BYTE:
                    data_str = self.pico_usb.read(rx_data_size-1)
                    start_byte_found=True
           
            hash = self.calc_crc(data_str)
            if hash == data_str[-1]:
                self.pico_usb.reset_input_buffer()
                # print(data_str)
                self.process_data(data_str)
                return 
                
            count += 1
            print(f"data not matched,count: {count}")
            # print(data_str)
    
    def process_data(self,data_):
        imu_msg = Imu()
        data = np.zeros(10,dtype=np.float64)
        data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9] , hash = struct.unpack("ddddddddddc", data_)
        
        #  Assign header values to the imu_msg
        imu_msg.header.frame_id="base_link"
        imu_msg.header.stamp=self.get_clock().now().to_msg()

        # Assign actuall values to the imu_msg
        imu_msg.orientation.w = data[0]
        imu_msg.orientation.x = data[1]
        imu_msg.orientation.y = data[2]
        imu_msg.orientation.z = data[3]

        imu_msg.angular_velocity.x = data[4]
        imu_msg.angular_velocity.y = data[5]
        imu_msg.angular_velocity.z = data[6]


        imu_msg.linear_acceleration.x = data[7]
        imu_msg.linear_acceleration.y = data[8]
        imu_msg.linear_acceleration.z = data[9]

        imu_msg.orientation_covariance[0] = 0.00121847
        imu_msg.orientation_covariance[1] = 0.0
        imu_msg.orientation_covariance[2] = 0.0
        imu_msg.orientation_covariance[3] = 0.0
        imu_msg.orientation_covariance[4] = 0.00121847
        imu_msg.orientation_covariance[5] = 0.0
        imu_msg.orientation_covariance[6] = 0.0
        imu_msg.orientation_covariance[7] = 0.0
        imu_msg.orientation_covariance[8] = 0.00121847

        imu_msg.angular_velocity_covariance[0] = 4.4944
        imu_msg.angular_velocity_covariance[1] = 0.0
        imu_msg.angular_velocity_covariance[2] = 0.0
        imu_msg.angular_velocity_covariance[3] = 0.0
        imu_msg.angular_velocity_covariance[4] = 4.4944
        imu_msg.angular_velocity_covariance[5] = 0.0
        imu_msg.angular_velocity_covariance[6] = 0.0
        imu_msg.angular_velocity_covariance[7] = 0.0
        imu_msg.angular_velocity_covariance[8] = 4.4944

        imu_msg.linear_acceleration_covariance[0] = 0.25
        imu_msg.linear_acceleration_covariance[1] = 0.0
        imu_msg.linear_acceleration_covariance[2] = 0.0
        imu_msg.linear_acceleration_covariance[3] = 0.0
        imu_msg.linear_acceleration_covariance[4] = 0.25
        imu_msg.linear_acceleration_covariance[5] = 0.0
        imu_msg.linear_acceleration_covariance[6] = 0.0
        imu_msg.linear_acceleration_covariance[7] = 0.0
        imu_msg.linear_acceleration_covariance[8] = 0.25

        # Publish message
        self.imu_publisher.publish(imu_msg)



    def calc_checksum(self, data=[]):
        for i in range(0,len(data)):
            checksum = checksum ^ data[i]
        return checksum

    def calc_crc(self, data=[]):
        hash_func=crc8()
        hash_func.update(data[0:-1])
        return hash_func.digest()[0]
    

def main(args=None):
    rclpy.init()
    serial_node = pico_imu_node()
    try:
        rclpy.spin(serial_node)
    except KeyboardInterrupt:  
        pass
    rclpy.shutdown()
   
if __name__ =='__main':
    main()

