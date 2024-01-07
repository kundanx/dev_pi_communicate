#! /usr/bin/env python3
import rclpy
import struct

from rclpy.node import Node 
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
        self.get_logger().info("Recieving data")
        
    # Read callback function
    def serial_read_callback(self):
            
            data = self.usb_port.read_data()
            # print(data)
            dist_x, dist_y, theta, vel_x, vel_y, omega, hash= struct.unpack('ffffffc', data)

            odometry_data = Pose()
            odometry_data.position.x = dist_x
            odometry_data.position.y=dist_y
            odometry_data.position.z=0.0
            odometry_data.orientation.x=0.0
            odometry_data.orientation.y=0.0
            odometry_data.orientation.z=0.0
            odometry_data.orientation.w=theta

            self.recieved_data_pub.publish(odometry_data)
            # print(" ")
            # serial_come.serial_port.kill()
            self.get_logger().info(str(odometry_data))

    # Joystick read callback function
    def send_joy_data(self,msg:Float32MultiArray):
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
        print(joy_data)
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
