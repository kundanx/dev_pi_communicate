#! /usr/bin/env python3
import rclpy
import struct

from rclpy.node import Node 
from geometry_msgs.msg import Pose

from dev_pi_communicate import serial_come

START_BYTE = 0xA5

class Serial_comms_node(Node):
    
    def __init__(self):

        super().__init__("serial_comm_node")

        self.recieved_data_pub = self.create_publisher(Pose,'/base_odom_topic', 10)
        self.create_timer(0.5, self.serial_read_callback)
        self.get_logger().info("Recieving data")
        
        
    # callback function to read data from serial port
    def serial_read_callback(self):
            
            data = serial_come.serial_port.read()
            print(data)
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
            print(" ")
            # serial_come.serial_port.kill()
            # self.get_logger().info(str(odometry_data))
    

def main(args=None):
    rclpy.init()
    serial_node = Serial_comms_node()
    rclpy.spin(serial_node)
    serial_come.serial_port.kill()  
    rclpy.shutdown()
   
if __name__ =='__main':
    main()
