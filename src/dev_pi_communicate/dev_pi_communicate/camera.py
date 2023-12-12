#! /usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
from dev_pi_communicate.serial_comm_node import serial_comms

class camera(Node):
    
    def __init__(self):
        super().__init__("camera_node")

        self.ball_horz_angle = 0.0
        self.ball_dimension = 0.0
        self.serial_baudrate = 9600
        self.serial_port='/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A50285BI-if00-port0'

        self.serial_comms_interface = serial_comms(
            self.serial_port,
            self.serial_baudrate
        )
        self.camera_node = self.create_subscription(
            Float32,
            "/ball_pos_topic",
            self.camera_callback ,
            10
        )
        self.get_logger().info("camera_node started")
    
    def camera_callback(self, value:Float32):
        self.ball_horz_angle = value
        # self.ball_dimension = data[1]
        # print(f"{self.ball_dimension} + {self.ball_horz_angle}")
        print(value)
        self.serial_comms_interface.send_camera_data(value.data)
  


def main( args = None):
    rclpy.init()
    node=camera()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ =="__main":
    main()