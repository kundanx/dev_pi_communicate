#! /usr/bin/env python3

# -------------------------SERIAL BRIDGE BETWEEN RASP PI AND STM32-------------------------------
# This node subscribes to
#   I) 'cmd_robot'_vel topic to recieve velocity commands 
#   II) 'act_vel' from BT to recieve actuator control signals, and  write the data to stm discovery

# This node reads odometry value from bluepill and publish the data on
#   I) 'freewheel/odom' topic to ekf filter package through
#   II)'Ball_status' topic to BT

import rclpy
import struct
import message_filters
import time
import math

from math import sin, cos
from rclpy.node import Node 
from std_msgs.msg import UInt8
from sensor_msgs.msg import Imu
from nav_msgs.msg import Odometry
from std_msgs.msg import Float32MultiArray
from std_msgs.msg import UInt8MultiArray

from dev_pi_communicate.crc8 import crc8
from dev_pi_communicate.serial_comms import serial_comms

START_BYTE= 0b10100101
RECIEVE_SIZE = 1+24+24+1
TRANSMIT_SIZE = 1+15+1
serial_baudrate = 115200
serial_port_address_FTDI='/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A50285BI-if00-port0'
serial_port_address_black='/dev/serial/by-id/usb-1a86_USB2.0-Serial-if00-port0'
    
class Serial_comms_TX_node(Node):
    
    def __init__(self):

        super().__init__("serial_bridge")
        self.serial_port = serial_comms(serial_port_address_black, serial_baudrate, RECIEVE_SIZE, TRANSMIT_SIZE, "CRC")
        
        # cmd_vel_sub = message_filters.Subscriber(self, Float32MultiArray, "cmd_robot_vel", qos_profile=10)
        # act_vel_sub = message_filters.Subscriber(self, UInt8MultiArray, "act_vel",qos_profile= 10)

        # self.synchronizer = message_filters.ApproximateTimeSynchronizer((cmd_vel_sub,act_vel_sub ), 10, 0.1,allow_headerless=True)
        # self.synchronizer.registerCallback(self.Send_Data_CallBack_)

        self.cmd_vel_sub = self.create_subscription( Float32MultiArray,"cmd_robot_vel", self.send_cmd_vel_data,10 )   
        self.act_vel_sub = self.create_subscription(UInt8MultiArray,"act_vel", self.send_act_vel_data,10 )
        self.cmd_vel_msg= Float32MultiArray()
        self.cmd_vel_rx_flag = False
        self.cmd_vel_msg.data = [0.0, 0.0, 0.0]
        self.act_vel_msg = UInt8MultiArray()
        # self.act_vel_rx_flag = False
        self.act_vel_msg.data = [0,0,0]
        self.timer2 = self.create_timer(0.05, self.Send_Data_CallBack)

        # self.ballStatus = self.create_publisher(UInt8, 'Ball_status', 10)
        self.odom_publisher_ = self.create_publisher(Odometry, 'odometry/filtered', 10)
        self.imu_publisher = self.create_publisher(Imu, 'imu/odom', 10)
        self.timer1 = self.create_timer(0.015, self.serial_read_callback)

        self.last_transmit_time = time.time()
        self.last_published_time = time.time()
        self.get_logger().info("Serial bridge ready...")
    
    # Joystick read callback function
    def Send_Data_CallBack(self):  
        # if not self.act_vel_rx_flag:
        #     self.act_vel_msg.data = [0,0,0]

        if not self.cmd_vel_rx_flag:
            self.cmd_vel_msg.data = [0.0, 0.0, 0.0]

        DataToSend=[
            bytes(struct.pack("B",START_BYTE)),
            bytes(struct.pack("f",self.cmd_vel_msg.data[0])),
            bytes(struct.pack("f",self.cmd_vel_msg.data[1])),
            bytes(struct.pack("f",self.cmd_vel_msg.data[2])),

            bytes(struct.pack("B",self.act_vel_msg.data[0])),
            bytes(struct.pack("B",self.act_vel_msg.data[1])),
            bytes(struct.pack("B",self.act_vel_msg.data[2]))
        ]
        DataToSend = b''.join(DataToSend)
        data_hash=self.calculate_crc(DataToSend[1:])
        # print(f"{data_hash =}")
        DataToSend=[
            DataToSend,
            bytes(struct.pack('B', data_hash)) 
        ]
        DataToSend=b''.join(DataToSend)
        diff_tx = time.time() - self.last_transmit_time
        # print(f"{diff_tx = }")
        self.last_transmit_time = time.time()
        # print(DataToSend)
        self.serial_port.write_data(DataToSend)
        self.cmd_vel_rx_flag = False
        self.act_vel_rx_flag = False
        # print(f"{self.act_vel_msg.data[2]=}")


    def send_act_vel_data(self, act_vel_msg_:UInt8MultiArray):
        self.act_vel_msg.data[0] = act_vel_msg_.data[0]
        self.act_vel_msg.data[1] = act_vel_msg_.data[1]
        self.act_vel_msg.data[2] = act_vel_msg_.data[2]
        # self.act_vel_rx_flag = True
        
    def send_cmd_vel_data(self, cmd_vel_msg_:Float32MultiArray):
        self.cmd_vel_msg.data[0] = cmd_vel_msg_.data[0]
        self.cmd_vel_msg.data[1] = cmd_vel_msg_.data[1]
        self.cmd_vel_msg.data[2] = cmd_vel_msg_.data[2]
        self.cmd_vel_rx_flag = True

    def serial_read_callback(self):
        _data = self.serial_port.read_data()
        # now = time.time()
        # diff =  now - self.last_published_time
        # print(f"{diff =}")
        # self.last_published_time = time.time()
        if _data == None:
            return

        '''data = [x, y, theta, vx, vy, omega, imu_data[6]]'''
        data = struct.unpack("ffffffffffff", _data[0:-1])
        self.process_odom(data[0:6])
        self.process_imu(data[6:])

        
            
    '''
    data:[pos_x, pose_y, theta, vel_x, vel_y, vel_z]
    '''
    def process_odom(self, data):
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
        print(f"pos_x:{data[0]}, pos_y:{data[1]}, yaw:{data[2]}")

    '''
    data: [yaw, pitch, roll, accel_x, accel_y,accel-z]
    '''
    def process_imu(self,data):
        imu_msg = Imu()    
        qw, qx, qy, qz = self.rollpitchyaw_to_quaternion(0.0, 0.0, data[0])
        #  Assign header values to the imu_msg
        imu_msg.header.stamp=self.get_clock().now().to_msg()
        imu_msg.header.frame_id="base_link"

        # Assign actuall values to the imu_msg
        imu_msg.orientation.w = qw
        imu_msg.orientation.x = qx
        imu_msg.orientation.y = qy
        imu_msg.orientation.z = qz

        imu_msg.angular_velocity.x = 0.0
        imu_msg.angular_velocity.y = 0.0
        imu_msg.angular_velocity.z = 0.0

        imu_msg.linear_acceleration.x = data[3]
        imu_msg.linear_acceleration.y = data[4]
        imu_msg.linear_acceleration.z = data[5]
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
        
        self.imu_publisher.publish(imu_msg)
        # print(f"{data[0]=},{data[1]=}, {data[5]=}")




    def calculate_checksum(self , data = []):
        digest = int()
        for i in range(1,len(data)):
            digest += data[i]
        return int(digest)
    
    def calculate_crc(self, data=[]):
        hash_func=crc8()
        hash_func.update(data)
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
    node = Serial_comms_TX_node()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt: 
        node.serial_port.close()
        node.destroy_node()
        rclpy.try_shutdown()
        exit()

if __name__ =='__main':
    main()
