#! /usr/bin/env python3

import math
import numpy as np
import rclpy


from rclpy.node import Node

from tf2_ros import TransformBroadcaster
from geometry_msgs.msg import TransformStamped
from geometry_msgs.msg import Pose
from geometry_msgs.msg import PoseWithCovariance
from geometry_msgs.msg import PoseWithCovarianceStamped
from nav_msgs.msg import Odometry

from math import sin, cos, atan2, sqrt,  pi



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

    return q #[x, y, z, w]

def quaternion_to_yawpitchroll(w, x, y, z):
    # roll (x-axis rotation)
    sinr_cosp = 2 * (w * x + y * z)
    cosr_cosp = 1 - 2 * (x * x + y * y)
    roll = atan2(sinr_cosp, cosr_cosp)

    # pitch (y-axis rotation)
    sinp = sqrt(1 + 2 * (w * y - x * z))
    cosp = sqrt(1 - 2 * (w * y - x * z))
    pitch = 2 * atan2(sinp, cosp) - pi / 2

    # yaw (z-axis rotation)
    siny_cosp = 2 * (w * z + x * y)
    cosy_cosp = 1 - 2 * (y * y + z * z)
    yaw = atan2(siny_cosp, cosy_cosp)

    return  yaw, pitch, roll


class map_base_tf(Node):

    def __init__(self):
        super().__init__('map_baseLink_tf2_broadcaster')

        # Initialize the transform broadcaster
        self.tf_broadcaster = TransformBroadcaster(self)

        # cfor NAV2
        # self.subscription = self.create_subscription(
        #     PoseWithCovarianceStamped,
        #     '/amcl_pose',
        #     self.handle_map,
        #     1)
        # self.get_logger().info(str("map to baseLink transform ready."))

        # for SLAM_TOOLBOX
        # self.subscription = self.create_subscription(
        #     PoseWithCovarianceStamped,
        #     '/pose',
        #     self.handle_map,
        #     1)

        self.subscription = self.create_subscription(
            Odometry,
            '/odometry/filtered',
            self.handle_map,
            1)
        self.get_logger().info(str("map to odom transform ready."))
        self.subscription  # prevent unused variable warning

    def handle_map(self, msg:Odometry):
        t = TransformStamped()

        # Read message content and assign it to
        # corresponding tf variables
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = 'map'
        t.child_frame_id = 'odom'

        # RObot moves only in 2D, thus we get x and y translation
        # coordinates from the message and set the z coordinate to 0
        t.transform.translation.x = 0.0
        t.transform.translation.y = 0.0
        t.transform.translation.z = 0.0

        # For the same reason, robot can only rotate around one axis
        # and this why we set rotation in x and y to 0 and obtain
        # rotation in z axis from the message

        t.transform.rotation.x = 0.0
        t.transform.rotation.y = 0.0
        t.transform.rotation.z = 0.0
        t.transform.rotation.w = 1.0
        
        # Send the transformation
        self.tf_broadcaster.sendTransform(t)

def main():
    rclpy.init()
    node = map_base_tf()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    rclpy.shutdown()