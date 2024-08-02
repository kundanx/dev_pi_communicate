#!/usr/bin/env python3

import rclpy 
import time
from rclpy.node import Node 
from std_msgs.msg import Bool
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import Float32MultiArray
from std_msgs.msg import UInt8MultiArray
from nav_msgs.msg import Odometry

from nav_msgs.msg import Odometry

## HELLO WORLD

class publisher(Node):

  
    def __init__(self):
        
        super().__init__("publisher_node")
        # self.data = PoseStamped()
        self.counter =0.0
        self.cmd_vel_pub =self.create_publisher(Float32MultiArray,"cmd_robot_vel", 50)
        self.silo_num_pub =self.create_publisher(UInt8MultiArray,"/silo_number", 50)
        self.cmd_pub = self.create_publisher(PoseStamped,"/ball_pose_topic", 10)
        self.flag_pub = self.create_publisher(Bool,"/is_ball_tracked", 10)
        self.odom_publisher_ = self.create_publisher(Odometry, 'odometry/filtered', 10)

        self.create_timer(0.05, self.publisher_callback)
        self.last_time = time.time()
        self.get_logger().info("Publishing command...")

    def publisher_callback(self):
        silo_num = UInt8MultiArray()
        silo_num.data = [3, 2]
        # print(f"{silo_num.data =}")
        
        now = time.time()
        diff = now - self.last_time
        self.last_time = now
        print(f"{diff = }")
        self.silo_num_pub.publish(silo_num)

    def send_ball_pose(self):
        self.data = PoseStamped()

        self.data.header.frame_id="map"
        
        self.data.pose.position.x = 0.20
        self.data.pose.position.y = 0.0
        self.data.pose.position.z = 0.0

        self.data.pose.orientation.x=0.0
        self.data.pose.orientation.y = 0.0
        self.data.pose.orientation.z = 0.0
        self.data.pose.orientation.w = 1.0

        self.flag = Bool()
        self.flag.data = True

        self.cmd_pub.publish(self.data)
        self.flag_pub.publish(self.flag)

        # data1 = UInt8MultiArray()
        # data1.data =[50, 50,0]
        # self.act_vel_pub.publish(data1)

        self.get_logger().info(str(self.data.pose.position.x))
        self.get_logger().info(str(self.flag.data))
    
    def send_cmd_act_vel(self):
        data1 = UInt8MultiArray()
        data1.data =[80, 80,3]
        self.act_vel_pub.publish(data1)

        # data2 = Float32MultiArray()
        # data2.data =[1.0, 1.0, 0.0]
        # self.cmd_vel_pub.publish(data2)
    
    def send_odom(self):
        odom_msg = Odometry()
        odom_msg.header.stamp = self.get_clock().now().to_msg()
        odom_msg.header.frame_id = 'odom'
        odom_msg.child_frame_id = 'base_link'
        odom_msg.pose.pose.position.x = 0.0
        odom_msg.pose.pose.position.y = 0.0
        odom_msg.pose.pose.position.z = 0.0
        # qw, qx, qy, qz = self.rollpitchyaw_to_quaternion(0.0, 0.0, 0.0)
        odom_msg.pose.pose.orientation.w = 1.0
        odom_msg.pose.pose.orientation.x = 0.0
        odom_msg.pose.pose.orientation.y = 0.0
        odom_msg.pose.pose.orientation.z = 0.0
        odom_msg.pose.covariance = [0.01, 0.0, 0.0, 0.0, 0.0, 0.0,
                                    0.0, 0.01, 0.0, 0.0, 0.0, 0.0,
                                    0.0, 0.0, 1.0, 0.0, 0.0, 0.0,
                                    0.0, 0.0, 0.0, 1.0, 0.0, 0.0,
                                    0.0, 0.0, 0.0, 0.0, 1.0, 0.0,
                                    0.0, 0.0, 0.0, 0.0, 0.0, 0.030461]
        odom_msg.twist.twist.linear.x = 1.0
        odom_msg.twist.twist.linear.y = 0.0
        odom_msg.twist.twist.linear.z = 0.0
        odom_msg.twist.twist.angular.x = 0.0
        odom_msg.twist.twist.angular.y = 0.0
        odom_msg.twist.twist.angular.z = 0.0
        odom_msg.twist.covariance = [0.25, 0.0, 0.0, 0.0, 0.0, 0.0,
                                        0.0, 0.25, 0.0, 0.0, 0.0, 0.0,
                                        0.0, 0.0, 1.0, 0.0, 0.0, 0.0,
                                        0.0, 0.0, 0.0, 1.0, 0.0, 0.0,
                                        0.0, 0.0, 0.0, 0.0, 1.0, 0.0,
                                        0.0, 0.0, 0.0, 0.0, 0.0, 0.04]
        self.odom_publisher_.publish(odom_msg)


        # self.counter= self.counter + 1 

def main(args=None):
    rclpy.init(args=args)
    node = publisher()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__=='__main__':
    main()