#!/usr/bin/env python3

import rclpy 
import time
from rclpy.node import Node 
from std_msgs.msg import String



class publisher(Node):
    
    def __init__(self):
        super().__init__("publisher_node")
        self.cmd_pub = self.create_publisher(String,"/charcter_topic", 10)
        self.create_timer(0.5, self.send_velocity_command)
        self.get_logger().info("publishing message:")
    
    
    def send_velocity_command(self):
        msg= String()
        msg.data = 'publishing data'
        self.cmd_pub.publish(msg)




def main(args=None):
    rclpy.init(args=args)
    node = publisher()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__=='__main__':
    main()