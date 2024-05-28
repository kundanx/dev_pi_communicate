#! /usr/bin/env python3

# This node recieves cmd_vel from nav2 packages and publishes data to serial_tx_node in packet form

import numpy as np
import rclpy
import sys
from pympler import asizeof

from rclpy.node import Node
from rclpy.qos import QoSReliabilityPolicy, QoSProfile
from geometry_msgs.msg import Twist
from std_msgs.msg import Float32MultiArray
from std_msgs.msg import Float64MultiArray

class cmdVel_to_serialBridge(Node):
    def __init__(self):
        super().__init__("cmdVel_to_serialBridge_node")
        qos_profile = QoSProfile(depth= 10)
        qos_profile.reliability = QoSReliabilityPolicy.BEST_EFFORT

        self.nav2_cmdvel_subscriber_node = self.create_subscription(
            Twist,
            "cmd_vel",
            self.nav2_recieve_callback,
            qos_profile)
        self.linefollow_cmdvel_subscriber_node = self.create_subscription(
            Twist,
            "cmd_vel/linefollow",
            self.linefollow_recieve_callback,
            qos_profile)
        self.cmd_pub= self.create_publisher(Float32MultiArray,"/cmd_robot_vel",qos_profile)
        self.get_logger().info("nav2_cmd_vel node ready ...")

    def nav2_recieve_callback(self, msg:Twist):

        twist_array = Float32MultiArray()
        twist_array.data = [float(msg.linear.x),float(msg.linear.y),float(msg.angular.z)]
        self.cmd_pub.publish(twist_array)
    
    def linefollow_recieve_callback(self, msg:Twist):
        twist_array = Float32MultiArray()
        twist_array.data = [float(msg.linear.x),float(msg.linear.y),float(msg.angular.z)]
        # print(f"ang.z: {msg.angular.z}")
        self.cmd_pub.publish(twist_array)

def main(args=None):
    rclpy.init()
    node = cmdVel_to_serialBridge()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:  
        pass
    rclpy.shutdown()
   
if __name__ =='__main':
    main()