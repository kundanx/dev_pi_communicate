#! /usr/bin/env python3
import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Float32MultiArray

class nav2_cmd_vel(Node):
    def __init__(self):
        super().__init__("cmd_vel_subscriber")
        self.subscriber_node = self.create_subscription(
            Twist,
            "cmd_vel",
            self.recieve_callback,
            10)
        self.cmd_pub= self.create_publisher(Float32MultiArray,"/cmd_robot_vel",10)
        self.get_logger().info("nav2_cmd_vel node ready ...")

    def recieve_callback(self, msg:Twist):
        twist_array = Float32MultiArray()
        twist_array.data = [msg.linear.x,msg.linear.y,msg.angular.z]
        self.cmd_pub.publish(twist_array)
        print(twist_array.data)

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