#!/usr/bin/env python3

import rclpy 
import time
from rclpy.node import Node 
from std_msgs.msg import String



class publisher(Node):

    counter =0
    vel_cmd = String()
    recieve_data_cml = String()
    def __init__(self):
        
        super().__init__("publisher_node")
        self.recieve_data = self.create_subscription(String, "recieve_data", self.recieve_cml_callback, 10)
        self.cmd_pub = self.create_publisher(String,"/string_topic", 10)
        self.create_timer(0.5, self.send_velocity_command)
        self.get_logger().info("Publishing command")
    
    def recieve_cml_callback(self, recieve_data_cml:String ):
        self.get_logger().info(self.recieve_data_cml)
        self.vel_cmd = self.recieve_data_cml
        
    
    def send_velocity_command(self):
        # self.vel_cmd.data = "publishing data" + str(self.counter)
        self.cmd_pub.publish(self.vel_cmd)
        self.counter= self.counter +1

def main(args=None):
    rclpy.init(args=args)
    node = publisher()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__=='__main__':
    main()