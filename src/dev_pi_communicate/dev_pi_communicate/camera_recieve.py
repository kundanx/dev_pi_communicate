#! /usr/bin/env python3

import rclpy
from rclpy.node import Node

from std_msgs.msg import Float32MultiArray

from dev_pi_communicate.serial_comm_node import serial_comms
from dev_pi_communicate.camera import base_vel
from dev_pi_communicate.camera import packet_to_send_camera

BALL_PIXELS = 140


class camera(Node):
    
    def __init__(self):
        super().__init__("camera_node")

        self.ball_horz_angle = 0.0
        self.ball_dimension = 0.0
        self.serial_baudrate = 115200
        self.base_vel = base_vel()
        self.packet_to_send = packet_to_send_camera()

        self.serial_port='/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A50285BI-if00-port0'

        self.serial_comms_interface = serial_comms(
            self.serial_port,
            self.serial_baudrate
        )
        self.camera_node = self.create_subscription(
            Float32MultiArray,
            "/ball_pos_topic",
            self.camera_callback ,
            10
        )
        self.get_logger().info("camera_node started")
    
    def camera_callback(self, msg):
        self.ball_horz_angle = msg.data[0] 
        self.ball_dimension = msg.data[1]
        self.compute_velocity()
        self.packet_to_send.create_packet(self.base_vel)
        self.serial_comms_interface.send_camera_data(self.packet_to_send)
    

    def compute_velocity(self):
        self.base_vel.vel_y = 0.0
        if self.ball_horz_angle > 5:
            self.base_vel.omega = 1
            self.base_vel.vel_x= 0.0
        elif self.ball_horz_angle < -5:
            self.base_vel.omega = -1
            self.base_vel.vel_x= 0.0
        elif self.ball_horz_angle > 0 and self.ball_horz_angle < 5:
            self.base_vel.omega = 0.5
            self.base_vel.vel_x= 0.0
        elif self.ball_horz_angle > -5 and self.ball_horz_angle < -0.0:
            self.base_vel.omega = -0.5
            self.base_vel.vel_x= 0.0

        if self.ball_horz_angle > -0.5 and self.ball_horz_angle < 0.5:
            self.base_vel.omega = -0.5
            if self.ball_dimension < 90:
                self.base_vel.vel_x = 1.0
            elif self.ball_dimension >= 90 and self.ball_dimension < 120:
                self.base_vel.vel_x = 0.5
            elif self.ball_dimension >= 120 and self.ball_dimension < BALL_PIXELS:
                self.base_vel.vel_x = 0.3
            elif self.ball_dimension == BALL_PIXELS:
                self.base_vel.vel_x= 0.0
            elif self.ball_dimension > BALL_PIXELS+50:
                self.base_vel.vel_x = -0.1
            elif self.ball_dimension > BALL_PIXELS+ 20 and self.ball_dimension <= BALL_PIXELS+50:
                self.base_vel.vel_x = -0.5
            elif self.ball_dimension <= BALL_PIXELS+20:
                self.base_vel.vel_x= -0.3
        if self.ball_dimension == 1000:
            self.base_vel.vel_x= 0.0
            self.base_vel.omega = 0.0
        
        print(self.base_vel.vel_x)
        print(self.base_vel.vel_x)
        print(self.base_vel.omega)
    


def main( args = None):
    rclpy.init()
    node=camera()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ =="__main":
    main()