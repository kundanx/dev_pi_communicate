#! /usr/bin/env python3
import math
import rclpy
from rclpy.node import Node
from std_msgs.msg import UInt8MultiArray

class Bt_Subscriber(Node):
    def __init__(self):
        super().__init__("Bt_subscriber_node")
        self.subscriber_to_filter_node = self.create_subscription(UInt8MultiArray, "act_vel", self.recieve_callback, 10)
    
    def recieve_callback(self, msg:UInt8MultiArray):
        # msg = [Roll_Speed, Conv_Speed, Roll_stats, conv_stats, pneumatic_stats ]
        msg_= UInt8MultiArray()
        msg_.data[0]=msg.data[0]
        msg_.data[1]=msg.data[1]
        msg_.data[2]=0x00
        if msg.data[2] == 1:
            msg_.data[2] = msg_.data[2] | 0b00000001
        
        if msg.data[3] == 1:
            msg_.data[2] = msg_.data[2] | 0b00000010
        
        if msg.data[4] == 1:
            msg_.data[2] = msg_.data[2] | 0b00000100
            


def main(args=None):
    rclpy.init()
    node = Bt_Subscriber()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ ==' __main__':
    main()


