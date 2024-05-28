#!/usr/bin/env python3

import rclpy 
from rclpy.qos import QoSReliabilityPolicy, QoSProfile

from rclpy.node import Node 
from std_msgs.msg import Bool
from std_msgs.msg import UInt8
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import Float32MultiArray
from std_msgs.msg import UInt8MultiArray
from nav_msgs.msg import Odometry

from nav_msgs.msg import Odometry

## HELLO WORLD

class publisher(Node):

  
    def __init__(self):
        
        super().__init__("publisher_node")

        qos_profile = QoSProfile(depth= 10)
        qos_profile.reliability = QoSReliabilityPolicy.BEST_EFFORT
        
        # self.data = PoseStamped()
        self.counter =0.0
        # self.cmd_vel_pub =self.create_publisher(Float32MultiArray,"cmd_robot_vel", 50)
        # self.act_vel_pub =self.create_publisher(UInt8MultiArray,"act_vel", 50)
        self.cmd_pub = self.create_publisher(PoseStamped,"/ball_pose_topic", qos_profile)
        self.flag_pub = self.create_publisher(Bool,"/is_ball_tracked", qos_profile)
        self.odom_publisher_ = self.create_publisher(Odometry, 'odometry/filtered', qos_profile)
        # self.junc_publisher = self.create_publisher(UInt8, 'junction_type', qos_profile)
        self.silo_publisher = self.create_publisher(UInt8, 'silo_number', qos_profile)
        self.area_3_reached_pub = self.create_publisher(UInt8, 'area_topic', qos_profile)



        self.create_timer(0.02, self.send_ball_pose)
        self.get_logger().info("Publishing command...")

    def area_3_reached(self):
        msg = UInt8()
        msg.data = 0XA5
        self.area_3_reached_pub.publish(msg)


    def send_ball_pose(self):
        self.data = PoseStamped()

        self.data.header.frame_id="map"
        
        self.data.pose.position.x = 0.0
        self.data.pose.position.y = 0.0
        self.data.pose.position.z = 0.0

        self.data.pose.orientation.x=0.0
        self.data.pose.orientation.y = 0.0
        self.data.pose.orientation.z = 0.0
        self.data.pose.orientation.w = 1.0

        self.flag = Bool()
        self.flag.data = True
        
        silo_num = UInt8()
        silo_num.data = 2

        junc_type = UInt8()
        junc_type.data = 4
        # self.junc_publisher.publish(junc_type)

        self.cmd_pub.publish(self.data)
        self.flag_pub.publish(self.flag)
        self.silo_publisher.publish(silo_num)


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