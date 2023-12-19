#! /usr/bin/env python3

import sys
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy
from dev_pi_communicate.joy import joy_buttons
from dev_pi_communicate.joy import packet_to_send_joy
from dev_pi_communicate import serial_come

    

class joy_node(Node):
    def __init__(self):
        super().__init__("joy_node")
        self.subscriber_node = self.create_subscription(Joy, "/joy", self.recieve_callback, 10)
        self.get_logger().info("Recieving command")

        self.packet_to_send = packet_to_send_joy()

        # object of class Serial for serial transmission
        # self.serial_baudrate = 115200
        # # self.serial_port='/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A50285BI-if00-port0'
        # global serial_comms_interface
        # self.serial_comms_interface = serial_comms( 
        #     '/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A50285BI-if00-port0',
        #     self.serial_baudrate
        # )
    
    def recieve_callback(self, msg:Joy):
        joy_bt= joy_buttons()

        joy_bt.button_A=msg.buttons[0]  
        joy_bt.button_B=msg.buttons[1]
        joy_bt.button_X=msg.buttons[2]
        joy_bt.button_Y=msg.buttons[3]

        joy_bt.button_LB=msg.buttons[4]
        joy_bt.button_RB=msg.buttons[5]

        joy_bt.button_stick_left=msg.buttons[11]
        joy_bt.button_stick_right=msg.buttons[12]

        joy_bt.axis_LT = msg.axes[2]
        joy_bt.axis_RT = msg.axes[5]
        
        joy_bt.axis_left_LR = msg.axes[0]
        joy_bt.axis_left_UD = msg.axes[1]
        joy_bt.axis_right_LR = msg.axes[3]
        joy_bt.axis_right_UD = msg.axes[4]

        joy_bt.mapping()
        self.packet_to_send.create_packet(joy_bt)
        serial_come.serial_port.send_joy_data(self.packet_to_send)

        
        
    
def main(args=None):
    rclpy.init()
    node = joy_node()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ ==' __main__':
    main()
