#!/usr/bin/env python3

import rclpy 
from rclpy.node import Node 
from std_msgs.msg import Float32MultiArray



class publisher(Node):

  
    def __init__(self):
        
        super().__init__("publisher_node")

        self.cmd_pub = self.create_publisher(Float32MultiArray,"/ball_pose_topic", 10)
        self.create_timer(0.5, self.send_velocity_command)
        self.get_logger().info("Publishing command")

    def send_velocity_command(self):
        self.angle=float
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