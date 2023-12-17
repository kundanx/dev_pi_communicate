#! /usr/bin/env python3

import rclpy
from rclpy.node import Node 
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Point
from dev_pi_communicate import serial_come


class vel_data:
    def __init__(self):
        self.linear_x=0.00
        self.linear_y=0.00
        self.linear_z=0.00

        self.angular_x=0.00
        self.angular_y=0.00
        self.angular_z=0.00

class teleop_key_node(Node):
    
    def __init__(self):
        # initiallize a node with namne: serial_comm_node
        super().__init__("serial_comm_node")
        self.data= vel_data()


        # self.recieved_data_pub = self.create_publisher(Point,'/recieved_data_topic', 10)
        # self.create_timer(0.5, self.serial_read_callback)
        # self.get_logger().info("Recieving data")
       
        # subsrcriber to listen data from terminal
        self.cmd_vel_sub = self.create_subscription(
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

        serial_come.serial_port.send_vel(self.data.linear_x, self.data.linear_y, self.data.linear_z,
                                        self.data.angular_x, self.data.angular_y, self.data.angular_z)
        # serial_come.serial_port.write_data()

def main(args=None):
    rclpy.init()
    teleop_node = teleop_key_node()
    rclpy.spin(teleop_node)
    rclpy.shutdown()
   
if __name__ =='__main':
    main()