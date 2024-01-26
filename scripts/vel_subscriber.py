#! /usr/bin/env python3

# Node to view velocity of robot according to ekf filter package

import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist

class subscriber(Node):
    def __init__(self):
        super().__init__("subscriber_node")
        self.subscription = self.create_subscription(
            Odometry,
            'odometry/filtered', #base_odom_topic'
            self.call_back,
            50)
        self.get_logger().info("Subrcribed to odometry/filtered")
    
    def call_back(self,msg:Odometry):
        msg_vel=Twist()
        msg_vel.linear.x = msg.twist.twist.linear.x
        msg_vel.linear.y = msg.twist.twist.linear.y
        msg_vel.linear.z = msg.twist.twist.linear.z

        msg_vel.angular.x = msg.twist.twist.linear.x
        msg_vel.angular.y = msg.twist.twist.linear.y
        msg_vel.angular.z = msg.twist.twist.linear.z
        self.get_logger().info(msg_vel)
        

def main(args=None):
    rclpy.init()
    node = subscriber()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ ==' __main__':
    main()
