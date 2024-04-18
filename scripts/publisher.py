#!/usr/bin/env python3

import rclpy 
from rclpy.node import Node 
from std_msgs.msg import Bool
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import Float32MultiArray

from nav_msgs.msg import Odometry

## HELLO WORLD

class publisher(Node):

  
    def __init__(self):
        
        super().__init__("publisher_node")
        # self.data = PoseStamped()
        self.counter =0.0
        self.publisher_ =self.create_publisher(Float32MultiArray,"/cmd_robot_vel", 50)
        self.cmd_pub = self.create_publisher(PoseStamped,"/ball_pose_topic", 10)
        self.flag_pub = self.create_publisher(Bool,"/is_ball_tracked", 10)
        self.create_timer(0.05, self.float32mut)
        self.get_logger().info("Publishing command...")

    def send_velocity_command(self):
        self.data = PoseStamped()

        self.data.header.frame_id="map"
        
        self.data.pose.position.x = 0.7
        self.data.pose.position.y = 0.5
        self.data.pose.position.z = 0.0

        self.data.pose.orientation.x=0.0
        self.data.pose.orientation.y = 0.0
        self.data.pose.orientation.z = 0.0
        self.data.pose.orientation.w = 1.0

        self.flag = Bool()
        self.flag.data = True

        self.cmd_pub.publish(self.data)
        self.flag_pub.publish(self.flag)
        self.get_logger().info(str(self.data.pose.position.x))
        self.get_logger().info(str(self.flag.data))
    
    def float32mut(self):
        data_ = Float32MultiArray()
        data_.data =[1.0, 2.0, 3.0]
        self.publisher_.publish(data_)

        # self.counter= self.counter + 1 

def main(args=None):
    rclpy.init(args=args)
    node = publisher()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__=='__main__':
    main()