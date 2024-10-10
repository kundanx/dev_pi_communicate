#! /usr/bin/env python3

# This node recieves cmd_vel from nav2 packages and publishes data to serial_tx_node in packet form

import rclpy
from geometry_msgs.msg import Twist
from rclpy.node import Node
from rclpy.qos import QoSProfile, QoSReliabilityPolicy
from std_msgs.msg import Float32MultiArray, Float64MultiArray, Int8, UInt8

MAX_VEL_ = 1.75


class cmdVel_to_serialBridge(Node):
    def __init__(self):
        super().__init__("cmdVel_to_serialBridge_node")
        qos_profile = QoSProfile(depth=10)
        qos_profile.reliability = QoSReliabilityPolicy.BEST_EFFORT

        self.nav2_cmdvel_subscriber_node = self.create_subscription(
            Twist, "cmd_vel", self.nav2_recieve_callback, 10
        )
        self.linefollow_cmdvel_subscriber_node = self.create_subscription(
            Twist, "cmd_vel/linefollow", self.linefollow_recieve_callback, qos_profile
        )
        self.slow_down_subscriber = self.create_subscription(
            Int8, "ball_detected_slow_down", self.slow_down_callback, 10
        )
        self.nav_to_silo_subscriber = self.create_subscription(
            Int8, "go_to_silo", self.go_to_silo_callback, 10
        )
        self.cmd_pub = self.create_publisher(Float32MultiArray, "/cmd_robot_vel", 10)

        self.slow_down_flag: bool = False
        self.MAX_VEL = MAX_VEL_
        self.get_logger().info("nav2_cmd_vel node ready ...")

    def slow_down_callback(self, slow_down_msg: Int8):
        if slow_down_msg.data == 1:
            self.slow_down_flag = True
        else:
            self.slow_down_flag = False

    def go_to_silo_callback(self, msg: UInt8):
        if msg.data == 1:
            self.MAX_VEL = MAX_VEL_
        elif msg.data == 0:
            self.MAX_VEL = 1.0

    def linefollow_recieve_callback(self, msg: Twist):
        twist_array = Float32MultiArray()
        twist_array.data = [
            float(msg.linear.x),
            # 0.0,
            float(msg.linear.y),
            float(msg.angular.z),
        ]
        self.cmd_pub.publish(twist_array)

    def nav2_recieve_callback(self, msg: Twist):
        twist_array = Float32MultiArray()
        if not self.slow_down_flag:
            if abs(msg.linear.x) > 0.5:
                # if( abs(msg.linear.x) > 0.5):
                #     msg.linear.x = MAX_VEL *(msg.linear.x) / abs(msg.linear.x)
                # else:
                msg.linear.x = self.map(
                    msg.linear.x, -1.0, 1.0, -self.MAX_VEL, self.MAX_VEL
                )

            if abs(msg.linear.y) > 0.5:
                # if( abs(msg.linear.y) > 0.4):
                #     msg.linear.y = MAX_VEL *(msg.linear.y) / abs(msg.linear.y)
                # else:
                msg.linear.y = self.map(
                    msg.linear.y, -1.0, 1.0, -self.MAX_VEL, self.MAX_VEL
                )

        twist_array.data = [
            float(msg.linear.x),
            float(msg.linear.y),
            float(msg.angular.z),
        ]

        self.cmd_pub.publish(twist_array)

    def map(self, value, in_min, in_max, out_min, out_max):
        if in_min == in_max:
            raise ValueError("Input range cannot be zero")
        mapped_value = out_min + (
            (value - in_min) * (out_max - out_min) / (in_max - in_min)
        )
        return mapped_value


def main(args=None):
    rclpy.init()
    node = cmdVel_to_serialBridge()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    rclpy.shutdown()


if __name__ == "__main":
    main()
