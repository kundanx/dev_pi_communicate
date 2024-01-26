#! /usr/bin/env python3
import math
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from nav_msgs.msg import Odometry
from sensor_msgs.msg import Imu

class subscriber(Node):
    def __init__(self):
        super().__init__("subscriber_node")
        self.subscriber_to_filter_node = self.create_subscription(Odometry, "/odometry/filtered", self.recieve_callback_filter, 10)
        self.subscriber_to_imu_node = self.create_subscription (Imu, "/imu/data", self.recieve_callback_imu, 10)
        self.subscriber_to_freewheel_node = self.create_subscription(Odometry, "/freewheel/odom", self.recieve_callback_freewheel, 10)
        self.get_logger().info("Quaternion to RollPitchYaw....")
    
    def recieve_callback_filter(self, msg:Odometry):
        q =[msg.pose.pose.orientation.x,
            msg.pose.pose.orientation.y,
            msg.pose.pose.orientation.z,
            msg.pose.pose.orientation.w]
        
        rpy= self.quaternon_to_rollpitchyaw(q)
        yaw= rpy[2]*180/math.pi
        self.get_logger().info(f"yaw form filter: {yaw}")
    
    def recieve_callback_imu(self, msg:Imu):
        q =[msg.orientation.x,
            msg.orientation.y,
            msg.orientation.z,
            msg.orientation.w]
        
        rpy= self.quaternon_to_rollpitchyaw(q)
        yaw= rpy[2]*180/math.pi
        self.get_logger().info(f"yaw from Imu: {yaw}")
    
    def recieve_callback_freewheel(self, msg:Odometry):
        q =[msg.pose.pose.orientation.x,
            msg.pose.pose.orientation.y,
            msg.pose.pose.orientation.z,
            msg.pose.pose.orientation.w]
        
        rpy= self.quaternon_to_rollpitchyaw(q)
        yaw= rpy[2]*180/math.pi
        self.get_logger().info(f"yaw from Freewheel: {yaw}")
    
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
