#! /usr/bin/env python3

# Node to view velocity of robot according to ekf filter package

import rclpy
import math
from rclpy.node import Node
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Imu

class subscriber(Node):
    def __init__(self):
        super().__init__("odometry_checker_node")
        self.yaw =[0.0]*3
        self.subscription = self.create_subscription(
            Odometry,
            'odometry/filtered', #base_odom_topic'
            self.call_back_o,
            50)
        self.subscription = self.create_subscription(
            Imu,
            '/imu/data', #base_odom_topic'
            self.call_back_i,
            50)
        self.subscription = self.create_subscription(
            Odometry,
            'freewheel/odom', #base_odom_topic'
            self.call_back_f,
            50)
        self.create_timer(0.05, self.print)

        self.get_logger().info("Subrcribed to odometry/filtered")

    def print(self):
        print(f"yaw_odom:{self.yaw[0]}, yaw_imu:{self.yaw[1]}, yaw_filter:{self.yaw[0]}")
    
    def call_back_o(self,msg:Odometry ):
        q =[0]*4

        q[0]= msg.pose.pose.orientation.x
        q[1]= msg.pose.pose.orientation.y
        q[2]= msg.pose.pose.orientation.z
        q[3]= msg.pose.pose.orientation.w
        
        rpy = self.quaternon_to_rollpitchyaw(q)
        self.yaw[2]=rpy[2]* 180/3.145
    
    def call_back_i(self,msg:Imu ):
 
        q =[0]*4
       
        q[0]= msg.orientation.x
        q[1]= msg.orientation.y
        q[2]= msg.orientation.z
        q[3]= msg.orientation.w
        
        rpy = self.quaternon_to_rollpitchyaw(q)
        self.yaw[1]=rpy[2]* 180/3.145

    def call_back_f(self,msg:Odometry ):
       
        q =[0]*4
        
        q[0]= msg.pose.pose.orientation.x
        q[1]= msg.pose.pose.orientation.y
        q[2]= msg.pose.pose.orientation.z
        q[3]= msg.pose.pose.orientation.w
        
        rpy = self.quaternon_to_rollpitchyaw(q)
        self.yaw[0]=rpy[2] * 180/3.145

    def quaternon_to_rollpitchyaw(self,q):

        # roll (x-axis rotation)
        sinr_cosp = 2 * (q[3] * q[0] + q[1] * q[2])
        cosr_cosp = 1 - 2 * (q[0] * q[0] + q[1] * q[1])
        roll = math.atan2(sinr_cosp, cosr_cosp)

        # pitch (y-axis rotation)
        sinp = math.sqrt(1 + 2 * (q[3] * q[1] - q[0] * q[2]))
        cosp = math.sqrt(1 - 2 * (q[3] * q[1] - q[0] * q[2]))
        pitch = 2 * math.atan2(sinp, cosp) -math.pi / 2 

        #  yaw (z-axis rotation)
        siny_cosp = 2 * (q[3] * q[2] + q[0] * q[1])
        cosy_cosp = 1 - 2 * (q[1] * q[1] + q[2] * q[2])
        yaw = math.atan2(siny_cosp, cosy_cosp)

        return roll, pitch, yaw
        

def main(args=None):
    rclpy.init()
    node = subscriber()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ ==' __main__':
    main()
