#! /usr/bin/env python3

# This node reads the odom data from bluepill and publish the data to ekf filter package through
# freewheel/odom topic

import rclpy
import struct
import math
import time


from math import sin, cos, radians
from rclpy.node import Node 
from nav_msgs.msg import Odometry

from dev_pi_communicate.crc8 import crc8
from dev_pi_communicate.serial_comm import serial_comms

START_BYTE= 0b10100101
serial_baudrate = 115200
serial_port_address_FTDI='/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A50285BI-if00-port0'
serial_port_address_black='/dev/serial/by-id/usb-1a86_USB2.0-Serial-if00-port0'

class Serial_comms_RX_node(Node):
    
    def __init__(self):

        super().__init__("serial_comm_RX_node")
        self.usb_port1 = serial_comms(serial_port_address_black, serial_baudrate)
        
        #  Odom data publisher
        self.odom_publisher_ = self.create_publisher(Odometry, 'odometry/filtered', 10)
        self.create_timer(0.05, self.serial_read_callback)

        self.last_sent_time = time.time()
        self.odom_seq = 0
        self.get_logger().info("Recieving ready...")
        
    # Read callback function
    def serial_read_callback(self):
            # self.get_logger().info("here......")
            _data = self.usb_port1.read_data()
            if (time.time() - self.last_sent_time > 0.03):
                # data = [x, y, theta, vx, vy, omega,B_count, R_count, L_count]
                data = struct.unpack("ffffff", _data[0:-1])
                odom_msg = Odometry()
                odom_msg.header.stamp = self.get_clock().now().to_msg()
                odom_msg.header.frame_id = 'odom'
                odom_msg.child_frame_id = 'base_link'
                odom_msg.pose.pose.position.x = data[0]
                odom_msg.pose.pose.position.y = data[1]
                odom_msg.pose.pose.position.z = 0.0
                qw, qx, qy, qz = self.rollpitchyaw_to_quaternion(0.0, 0.0, data[2])
                odom_msg.pose.pose.orientation.w = qw
                odom_msg.pose.pose.orientation.x = qx
                odom_msg.pose.pose.orientation.y = qy
                odom_msg.pose.pose.orientation.z = qz
                odom_msg.pose.covariance = [0.01, 0.0, 0.0, 0.0, 0.0, 0.0,
                                            0.0, 0.01, 0.0, 0.0, 0.0, 0.0,
                                            0.0, 0.0, 1.0, 0.0, 0.0, 0.0,
                                            0.0, 0.0, 0.0, 1.0, 0.0, 0.0,
                                            0.0, 0.0, 0.0, 0.0, 1.0, 0.0,
                                            0.0, 0.0, 0.0, 0.0, 0.0, 0.030461]
                odom_msg.twist.twist.linear.x = data[3]
                odom_msg.twist.twist.linear.y = data[4]
                odom_msg.twist.twist.linear.z = 0.0
                odom_msg.twist.twist.angular.x = 0.0
                odom_msg.twist.twist.angular.y = 0.0
                odom_msg.twist.twist.angular.z = data[5]
                odom_msg.twist.covariance = [0.25, 0.0, 0.0, 0.0, 0.0, 0.0,
                                                0.0, 0.25, 0.0, 0.0, 0.0, 0.0,
                                                0.0, 0.0, 1.0, 0.0, 0.0, 0.0,
                                                0.0, 0.0, 0.0, 1.0, 0.0, 0.0,
                                                0.0, 0.0, 0.0, 0.0, 1.0, 0.0,
                                                0.0, 0.0, 0.0, 0.0, 0.0, 0.04]
                self.odom_publisher_.publish(odom_msg)
                self.odom_seq += 1
                self.last_sent_time = time.time()
                self.get_logger().info('"%f %f %f "'
                                       %(data[0], data[1], data[2]*180/math.pi))
                # print(f"pos_x:{data[0]}, pos_y:{data[1]}, yaw:{data[2]*180/math.pi}")
                # print(f"yaw:{data[2]*180/math.pi}")
                # self.get_logger().info("here1")
        

    def calculate_checksum(self , data = []):
        digest = int()
        for i in range(1,len(data)):
            digest += data[i]
        return int(digest)
    
    def calculate_crc(self, data=[]):
        hash_func=crc8()
        hash_func.update(data[1:])
        return hash_func.digest()[0]
    
    def rollpitchyaw_to_quaternion(self,roll, pitch, yaw):
        

        cy = cos(yaw * 0.5)
        sy = sin(yaw * 0.5)
        cp = cos(pitch * 0.5)
        sp = sin(pitch * 0.5)
        cr = cos(roll * 0.5)
        sr = sin(roll * 0.5)

        qw = cy * cp * cr + sy * sp * sr
        qx = cy * cp * sr - sy * sp * cr
        qy = sy * cp * sr + cy * sp * cr
        qz = sy * cp * cr - cy * sp * sr

        return qw, qx, qy, qz
    
    def quaternon_to_rollpitchyaw(self,q):

        # roll (x-axis rotation)
        sinr_cosp = 2 * (q[3] * q[0] + q[1] * q[2])
        cosr_cosp = 1 - 2 * (q[0] * q[0] + q[1] * q[1])
        roll = math.atan2(sinr_cosp, cosr_cosp)

        # pitch (y-axis rotation)
        sinp = math.sqrt(1 + 2 * (q[3] * q[1] - q[0] * q[2]))
        cosp = math.sqrt(1 - 2 * (q[3] * q[1] - q[0] * q[2]))
        pitch = 2 * math.atan2(sinp, cosp) -math.pi / 2 

        #  yaw (z-axis rotation)
        siny_cosp = 2 * (q[3] * q[2] + q[0] * q[1])
        cosy_cosp = 1 - 2 * (q[1] * q[1] + q[2] * q[2])
        yaw = math.atan2(siny_cosp, cosy_cosp)

        return roll, pitch, yaw
    

def main(args=None):
    rclpy.init()
    node = Serial_comms_RX_node()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:  
        pass
    rclpy.shutdown()
   
if __name__ =='__main':
    main()