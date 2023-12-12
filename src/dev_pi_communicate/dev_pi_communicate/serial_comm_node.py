#! /usr/bin/env python3
import rclpy
import serial
import struct
import sys

from pympler import asizeof
from rclpy.node import Node 
from std_msgs.msg import Float32
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist
from dev_pi_communicate.joy import packet_to_send

START_BYTE=bytes.fromhex('A5')

class vel_data:
    def __init__(self):
        self.linear_x=0.00
        self.linear_y=0.00
        self.linear_z=0.00

        self.angular_x=0.00
        self.angular_y=0.00
        self.angular_z=0.00

    
class serial_comms:
    def __init__(self, serial_port, serial_baudrate):
        self.serial = serial.Serial(serial_port, serial_baudrate)


    def send_vel(self, vel_x, vel_y, vel_z,ang_x,ang_y,ang_z):
        
        #data_to_send= struct.pack("f f f", vel_x, vel_y, vel_z) #  + struct.pack("f", vel_y)+struct.pack("f",vel_z)
        data_to_send = [
            bytes(struct.pack("f", vel_x)),
            bytes(struct.pack("f", vel_y)),
            bytes(struct.pack("f", vel_z)),
            bytes(struct.pack("f", ang_x)),
            bytes(struct.pack("f", ang_y)),
            bytes(struct.pack("f", ang_z))
            ]
        data_to_send = b''.join(data_to_send)
        data_to_send = START_BYTE + data_to_send
        print(data_to_send)
        print(f"{len(data_to_send)=}")
        self.serial.write(data_to_send)
        # return data_to_send
    
    def send_camera_data(self, camera_data):
        camera_data_to_send = [
            # bytes(struct.pack("f", camera_data[0])),
            bytes(struct.pack('f', camera_data))
        ]
        camera_data_to_send = b''.join(camera_data_to_send)
        camera_data_to_send = START_BYTE + camera_data_to_send
        print(camera_data_to_send)
        self.serial.write(camera_data_to_send)
    
    def send_joy_data(self, data= packet_to_send()):
        joy_data_to_send =[
            bytes(struct.pack("B",data.byte[0])),
            bytes(struct.pack("B",data.byte[1])),
            bytes(struct.pack("B",data.byte[2])),
            bytes(struct.pack("B",data.byte[3])),
            bytes(struct.pack("B",data.byte[4])),
            bytes(struct.pack("b",data.byte[5])),
            bytes(struct.pack("b",data.byte[6])),
            bytes(struct.pack("b",data.byte[7])),
            bytes(struct.pack("b",data.byte[8])),
            bytes(struct.pack("B",data.byte[9]))
        ]
        joy_data_to_send= b''.join(joy_data_to_send)
        # print(joy_data_to_send)
        self.serial.write(joy_data_to_send)
    
    def __del__(self):
        self.serial.close()
        

class Serial_comms_node(Node):
    
    def __init__(self):
        # initiallize a node with namne: serial_comm_node
        super().__init__("serial_comm_node")
        self.declare_parameter('usb_serial_port')
        self.data= vel_data()
       

        # object of class Serial for serial transmission
        self.serial_baudrate = 9600
        # self.serial_port='/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A50285BI-if00-port0'
        global serial_comms_interface
        self.serial_comms_interface = serial_comms( 
            '/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A50285BI-if00-port0',
            self.serial_baudrate
        )
        

        # subsrcriber to listen data from terminal
        self.subscriber = self.create_subscription(
            Twist,
            "cmd_vel",
            self.callback, 
            10
        )
        

    def callback(self,msg:Twist):

        self.data.linear_x= msg.linear.x
        self.data.linear_y= msg.linear.y
        self.data.linear_z= msg.linear.z

        self.data.angular_x=msg.angular.x
        self.data.angular_y=msg.angular.y
        self.data.angular_z=msg.angular.z

        self.serial_comms_interface.send_vel(self.data.linear_x, self.data.linear_y, self.data.linear_z,
                                             self.data.angular_x, self.data.angular_y, self.data.angular_z)
        self.get_logger().info(str(self.data.linear_x))
        

        
    

def main(args=None):
    rclpy.init()
    serial_node = Serial_comms_node()
    rclpy.spin(serial_node)
    rclpy.shutdown()
   
if __name__ =='__main':
    main()
