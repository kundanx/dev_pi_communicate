#! /usr/bin/env python3

# This node recieves cmd_vel from nav2 packages and publishes data to serial_tx_node in packet form

import numpy as np
import rclpy
import sys
from pympler import asizeof

from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Float32MultiArray
from std_msgs.msg import Float64MultiArray

class nav2_cmd_vel(Node):
    def __init__(self):
        super().__init__("nav2_cmd_vel")
        self.subscriber_node = self.create_subscription(
            Twist,
            "cmd_vel",
            self.recieve_callback,
            10)
        self.cmd_pub= self.create_publisher(Float32MultiArray,"/cmd_robot_vel",10)
        self.get_logger().info("nav2_cmd_vel node ready ...")

    def recieve_callback(self, msg:Twist):
        twist_array = Float32MultiArray()
        twist_array.data = [float(msg.linear.x),float(msg.linear.y),float(msg.angular.z)]
        # print(f"size{asizeof.asizeof(twist_array.data)}")
        self.cmd_pub.publish(twist_array)
        # print(twist_array.data)

def main(args=None):
    rclpy.init()
    node = nav2_cmd_vel()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:  
        pass
    rclpy.shutdown()
   
if __name__ =='__main':
    main()