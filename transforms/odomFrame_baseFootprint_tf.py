#! /usr/bin/env python3

import math
import numpy as np
import rclpy

from rclpy.node import Node

from tf2_ros import TransformBroadcaster
from geometry_msgs.msg import TransformStamped
from geometry_msgs.msg import Pose



def quaternion_from_euler(ai, aj, ak):
    ai /= 2.0
    aj /= 2.0
    ak /= 2.0
    ci = math.cos(ai)
    si = math.sin(ai)
    cj = math.cos(aj)
    sj = math.sin(aj)
    ck = math.cos(ak)
    sk = math.sin(ak)
    cc = ci*ck
    cs = ci*sk
    sc = si*ck
    ss = si*sk

    q = np.empty((4, ))
    q[0] = cj*sc - sj*cs
    q[1] = cj*ss + sj*cc
    q[2] = cj*cs - sj*sc
    q[3] = cj*cc + sj*ss

    return q


class odom_base_tf(Node):

    def __init__(self):
        super().__init__('odom_base_footprint_tf2_broadcaster')

        # Initialize the transform broadcaster
        self.tf_broadcaster = TransformBroadcaster(self)

        # callback function on each message
        self.subscription = self.create_subscription(
            Pose,
            'base_odom_topic',
            self.handle_odom,
            1)
        self.subscription  # prevent unused variable warning

    def handle_odom(self, msg):
        t = TransformStamped()

        # Read message content and assign it to
        # corresponding tf variables
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = 'odom_frame'
        t.child_frame_id = 'base_footprint'

        # RObot moves only in 2D, thus we get x and y translation
        # coordinates from the message and set the z coordinate to 0
        t.transform.translation.x = msg.position.x
        t.transform.translation.y = msg.position.y
        t.transform.translation.z = 0.0

        # For the same reason, robot can only rotate around one axis
        # and this why we set rotation in x and y to 0 and obtain
        # rotation in z axis from the message
        q = quaternion_from_euler(0, 0, msg.orientation.w)
        t.transform.rotation.x = q[0]
        t.transform.rotation.y = q[1]
        t.transform.rotation.z = q[2]
        t.transform.rotation.w = q[3]

        # Send the transformation
        self.tf_broadcaster.sendTransform(t)
        self.get_logger().info(str("Odom to base_Footprint transform published."))

def main():
    rclpy.init()
    node = odom_base_tf()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    rclpy.shutdown()