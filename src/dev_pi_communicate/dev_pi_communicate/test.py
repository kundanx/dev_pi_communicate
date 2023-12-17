#! /usr/bin/env python3
import rclpy
import struct

from rclpy.node import Node 
from geometry_msgs.msg import Point

from dev_pi_communicate import serial_come

START_BYTE = 0xA5

class Serial_comms_node(Node):
    
    def __init__(self):

        self.recieved_data_pub = self.create_publisher(Point,'/recieved_data_topic', 10)
        self.create_timer(0.5, self.serial_read_callback)
        self.get_logger().info("Recieving data")
        
        
    # callback function to read data from serial port
    def serial_read_callback(self):
            data = serial_come.serial_port.read()
            data= struct.unpack('BBBBBBBBB', data)

            odometry_data = Point()
            odometry_data.x=float(data[0])
            odometry_data.y=float(data[1])
            odometry_data.z=float(data[2])

            self.recieved_data_pub.publish(odometry_data)
            print(data)   

def main(args=None):
    rclpy.init()
    serial_node = Serial_comms_node()
    rclpy.spin(serial_node)
    rclpy.shutdown()
   
if __name__ =='__main':
    main()
