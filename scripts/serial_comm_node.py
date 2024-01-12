#! /usr/bin/env python3
import rclpy
import struct
import math
import time

from math import sin, cos, radians
from rclpy.node import Node 
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Pose
from std_msgs.msg import Float32MultiArray

from dev_pi_communicate.crc8 import crc8
from dev_pi_communicate import serial_comm
from dev_pi_communicate.serial_comm import serial_comms

START_BYTE= 0b10100101
serial_baudrate = 115200
serial_port_address_FTDI='/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A50285BI-if00-port0'
serial_port_address_black='/dev/serial/by-id/usb-1a86_USB2.0-Serial-if00-port0'

class Serial_comms_node(Node):
    
    def __init__(self):

        super().__init__("serial_comm_node")

        self.usb_port = serial_comms(serial_port_address_black, serial_baudrate)

        # Subscriber to joystick data
        self.sub_joy = self.create_subscription(
            Float32MultiArray,
            "/cmd_robot_vel",
            self.send_joy_data,
            10 )
        
        #  Odom data publisher
        self.recieved_data_pub = self.create_publisher(Pose,'/base_odom_topic', 20)

        self.create_timer(0.1, self.serial_read_callback)
        self.last_sent_time = time.time()
        self.odom_seq = 0
        self.get_logger().info("Recieving data")
        
    # Read callback function
    def serial_read_callback(self):
            
            _data = self.usb_port.read_data()

            if (time.time() - self.last_sent_time > 0.05):
                # data = [x, y, theta, vx, vy, omega]
                data = struct.unpack("ffffff", _data[0:24])
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
                self.get_logger().info('"%f %f %f %f %f %f"'
                                    %(data[0], data[1], data[2], data[3], data[4], data[5]))
                

    # Joystick read callback function
    def send_joy_data(self,msg:Float32MultiArray):
        # print("here recieve")
        joy_data=[
            bytes(struct.pack("B",START_BYTE)),
            bytes(struct.pack("f",msg.data[0])),
            bytes(struct.pack("f",msg.data[1])),
            bytes(struct.pack("f",msg.data[2]))
        ]
        joy_data = b''.join(joy_data)
        hash=self.calculate_crc(joy_data)
        joy_data=[joy_data,
            bytes(struct.pack('B', hash)) 
        ]
        joy_data=b''.join(joy_data)
        # print(joy_data)
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
    
    def rollpitchyaw_to_quaternion(self,roll, pitch, yaw):
        roll_rad = radians(roll)
        pitch_rad = radians(pitch)
        yaw_rad = radians(yaw)

        cy = cos(yaw_rad * 0.5)
        sy = sin(yaw_rad * 0.5)
        cp = cos(pitch_rad * 0.5)
        sp = sin(pitch_rad * 0.5)
        cr = cos(roll_rad * 0.5)
        sr = sin(roll_rad * 0.5)

        qw = cy * cp * cr + sy * sp * sr
        qx = cy * cp * sr - sy * sp * cr
        qy = sy * cp * sr + cy * sp * cr
        qz = sy * cp * cr - cy * sp * sr

        return qw, qx, qy, qz
    

def main(args=None):
    rclpy.init()
    serial_node = Serial_comms_node()
    try:
        rclpy.spin(serial_node)
    except KeyboardInterrupt:  
        pass
    rclpy.shutdown()
   
if __name__ =='__main':
    main()
