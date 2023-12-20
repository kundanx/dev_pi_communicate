#!/usr/bin/env python3

import rclpy 
from rclpy.node import Node 
from std_msgs.msg import Float32MultiArray
from geometry_msgs.msg import Pose



class publisher(Node):

  
    def __init__(self):
        
        super().__init__("publisher_node")
        self.data = Pose()
        self.counter =0.0
        self.cmd_pub = self.create_publisher(Pose,"/base_odom_topic", 10)
        self.create_timer(0.5, self.send_velocity_command)
        self.get_logger().info("Publishing command")

    def send_velocity_command(self):
        self.counter += 0.01
        self.data.position.x = self.counter
        self.data.position.y = self.counter
        self.data.position.z = self.counter
        self.data.orientation.x = 0.0
        self.data.orientation.y = 0.0
        self.data.orientation.z = 0.0
        self.data.orientation.w = 1.0
        self.cmd_pub.publish( self.data)
        # self.get_logger().info(str(self.vel_cmd))
        # self.counter= self.counter + 1 

def main(args=None):
    rclpy.init(args=args)
    node = publisher()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__=='__main__':
    main()