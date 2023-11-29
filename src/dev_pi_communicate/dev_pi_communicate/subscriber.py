#! /usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class subscriber(Node):
    def __init__(self):
        super().__init__("subscriber_node")
        self.subscriber_node = self.create_subscription(String, "/string_topic", self.recieve_callback, 10)
        self.get_logger().info("fuck me")
    
    def recieve_callback(self, msg:String):
        self.get_logger().info(str(msg))

def main(args=None):
    rclpy.init()
    node = subscriber()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ ==' __main__':
    main()
