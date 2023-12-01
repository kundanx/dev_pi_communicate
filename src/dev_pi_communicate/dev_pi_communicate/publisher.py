#!/usr/bin/env python3

import rclpy 
from rclpy.node import Node 
from std_msgs.msg import String



class publisher(Node):

  
    def __init__(self):
        
        super().__init__("publisher_node")

        self.counter =0
        self.vel_cmd = String()
        self.recieve_data_cml = String()

        self.cmd_pub = self.create_publisher(String,"/string_topic", 10)
        self.create_timer(0.5, self.send_velocity_command)
        self.get_logger().info("Publishing command")

        
    
    def send_velocity_command(self):
        self.vel_cmd.data =  "publishing data" + str(self.counter) 
        self.cmd_pub.publish( self.vel_cmd)
        self.get_logger().info(str(self.vel_cmd))
        self.counter= self.counter + 1 

def main(args=None):
    rclpy.init(args=args)
    node = publisher()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__=='__main__':
    main()