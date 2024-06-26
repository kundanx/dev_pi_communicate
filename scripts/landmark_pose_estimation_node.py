#! /usr/bin/env python3

"""
ROS2 Node to publish 2d pose estimate to robot_localization package.
This node subscribes to /silo_number{published by apil} and /junction_type{published by linefollower node}
This node publishes 2D Pose whenever T_junction is detected.
2D pose is determined on the basis of which silo is the robot is navigating to.
"""

import math
import os
from math import cos, sin

import rclpy
import yaml
from geometry_msgs.msg import PoseWithCovarianceStamped
from nav_msgs.msg import Odometry
from rclpy.node import Node
from rclpy.qos import QoSProfile, QoSReliabilityPolicy
from std_msgs.msg import Float64MultiArray, UInt8

"""
Junction euivalent Int ----------------------------
"""
JUNCTION_NOT_DETECTED = 0
LEFT_TURN = 1
RIGHT_TURN = 2
CROSS_JUNCTION = 3
T_JUNCTION = 4
RIGHT_T_JUNCTION = 5
LEFT_T_JUNCTION = 6
X_HORIZONTAL_LINE = 7
Y_VERTICAL_LINE = 8
L_JUNCTION = 9
MIRROR_L_JUNCTIO = 10
"""----------------------------------------------"""


class landmarkPoseEstimation(Node):
    def __init__(self) -> None:
        super().__init__("landmark_pose_estimation_node")

        qos_profile = QoSProfile(depth=10)
        qos_profile.reliability = QoSReliabilityPolicy.BEST_EFFORT

        self.raw_odometry_subs = self.create_subscription(
            Odometry, "odometry/raw", self.raw_odometry_subs, qos_profile
        )
        self.filtered_odometry_subs = self.create_subscription(
            Odometry, "odometry/filtered", self.odometry_callback, qos_profile
        )
        self.silo_number_subs = self.create_subscription(
            UInt8, "silo_number", self.siloNum_subscriber_callback, qos_profile
        )

        self.junctionType_subs = self.create_subscription(
            UInt8, "junction_type", self.junctionDetection_callback, qos_profile
        )
        self.on_which_Area_sub = self.create_subscription(
            UInt8, "area_reached", self.area3_reached_callback, 10
        )
        self.update_after_ball_storing_subs = self.create_subscription(
            UInt8, "alignedSilo_number", self.update_after_storing_ball, 10
        )

        self.pose2D_timer = self.create_timer(0.001, self.update_odometry)
        self.pose2D_pub = self.create_publisher(
            Float64MultiArray, "landmark_updates", 10
        )

        self.raw_odom_msg = Odometry()
        self.pose2D = [0] * 2
        self.junction_type = UInt8()
        self.silo_number: UInt8 = 0
        self.landMark_detected: bool = False
        self.is_on_silo_region: bool = False
        self.is_on_area3: bool = True
        self.ball_store_just_now: bool = False
        self.origin_reset_once: bool = False
        self.landmakr_update_count = 0

        """ Read YAML file """
        file_path = os.path.join(
            os.path.dirname(__file__), "..", "config/landmark_locations.yaml"
        )
        with open(file_path, "r") as stream:
            self.data_loaded = yaml.safe_load(stream)

        self.get_logger().info("landmark_pose_estimation_node ready...")

    def odometry_callback(self, msg: Odometry):
        if msg.pose.pose.position.y <= -1.8:
            self.is_on_silo_region = True
        elif msg.pose.pose.position.y > -1.8:
            self.is_on_silo_region = False

    def raw_odometry_subs(self, msg: Odometry):
        self.raw_odom_msg = msg
        # print(f"raw_y: {self.raw_odom_msg.pose.pose.position.y}")

    def siloNum_subscriber_callback(self, msg: UInt8) -> None:
        self.silo_number = msg.data

    def update_after_storing_ball(self, msg: UInt8):
        if msg.data == 1:
            self.pose2D = self.data_loaded["landmark_pose_estimation_node"]["silo_1"]

        elif msg.data == 2:
            self.pose2D = self.data_loaded["landmark_pose_estimation_node"]["silo_2"]

        elif msg.data == 3:
            self.pose2D = self.data_loaded["landmark_pose_estimation_node"]["silo_3"]

        elif msg.data == 4:
            self.pose2D = self.data_loaded["landmark_pose_estimation_node"]["silo_4"]

        elif self.silo_number == 5:
            self.pose2D = self.data_loaded["landmark_pose_estimation_node"]["silo_5"]

        self.ball_store_just_now = True
        print(f"UPDATE_AFTER_STORING_BALL:: aligned with silo {msg.data}")
        # breakpoint()

    def area3_reached_callback(self, msg: UInt8):
        if msg.data == 0xA5:
            self.is_on_area3 = True
            self.origin_reset_once = True
            self.pose2D = self.data_loaded["landmark_pose_estimation_node"][
                "area3_reset"
            ]
            print(f"AREA3_REACHED::")

    def junctionDetection_callback(self, msg: UInt8) -> None:
        self.junction_type.data = msg.data
        # if msg.data != 0:
        #     print(f"data: {msg.data}")
        if msg.data == T_JUNCTION:
            if self.silo_number == 1:
                self.pose2D = self.data_loaded["landmark_pose_estimation_node"][
                    "silo_1_TJunction"
                ]
                self.get_logger().info("sil0 1 T found")

            elif self.silo_number == 2:
                self.pose2D = self.data_loaded["landmark_pose_estimation_node"][
                    "silo_2_TJunction"
                ]
                # self.get_logger().info("silo 2 T found")
            elif self.silo_number == 3:
                self.pose2D = self.data_loaded["landmark_pose_estimation_node"][
                    "silo_3_TJunction"
                ]
                self.get_logger().info("silo 3 T found")

            elif self.silo_number == 4:
                self.pose2D = self.data_loaded["landmark_pose_estimation_node"][
                    "silo_4_TJunction"
                ]
                self.get_logger().info("silo 4 T found")

            # if self.silo_number != 0:
            self.silo_number = 0
            self.landMark_detected = False
            # print(f"isOnArea3: {self.is_on_area3}, isOnSiloRegion: {self.is_on_silo_region },isLandMarkDetected: {self.landMark_detected}")

            # breakpoint()

        elif msg.data == L_JUNCTION or msg.data == RIGHT_TURN:
            if self.silo_number == 5:
                self.pose2D = self.data_loaded["landmark_pose_estimation_node"][
                    "silo_5_RJunction"
                ]
                self.get_logger().info("silo 5 T found")
                self.silo_number = 0
                self.landMark_detected = False
                # breakpoint()

        elif msg.data == CROSS_JUNCTION:
            self.pose2D = self.data_loaded["landmark_pose_estimation_node"][
                "cross_junction"
            ]
            self.get_logger().info("Cross Junc found")
            self.landMark_detected = False
            # breakpoint()

        elif msg.data == X_HORIZONTAL_LINE:
            self.pose2D = self.data_loaded["landmark_pose_estimation_node"][
                "x_horizontal_line"
            ]
            self.landMark_detected = False
            self.get_logger().info("X_horizontal line found")
            # breakpoint()

        landMark_detected = False

    def update_odometry(self):
        if self.is_on_area3:
            if self.is_on_silo_region:
                ready_to_publish = False
                junc_type: float = 0.0
                if self.landMark_detected:
                    ready_to_publish = True
                    self.landMark_detected = False
                    junc_type = float(self.junction_type.data)
                    print("landmark_detected")

                elif self.ball_store_just_now:
                    ready_to_publish = True
                    self.ball_store_just_now = False
                    junc_type = float(CROSS_JUNCTION)
                    print("ball_stored_just_now")
                
                elif self.origin_reset_once == True:
                    ready_to_publish = True
                    self.origin_reset_once = False
                    junc_type = float(CROSS_JUNCTION)
                    print("Area3 Reached")

                if ready_to_publish == True:
                    x_offset = self.raw_odom_msg.pose.pose.position.x - self.pose2D[0]
                    y_offset = self.raw_odom_msg.pose.pose.position.y - self.pose2D[1]
                    self.landmakr_update_count += 1
                    msg = Float64MultiArray()
                    msg.data = [junc_type, x_offset, y_offset]
                    # print("Update_odometry :: ready_to_publish")
                    print(
                        f"raw_x: {self.raw_odom_msg.pose.pose.position.x}, raw_y: {self.raw_odom_msg.pose.pose.position.y}"
                    )
                    # print(f"isOnArea3: {self.is_on_area3}, isOnSiloRegion: {self.is_on_silo_region },isLandMarkDetected: {self.landMark_detected}")
                    print(
                        f"pose_x: {self.pose2D[0]}, pose_y: {self.pose2D[1]}, {x_offset= }, {y_offset= }"
                    )
                    # breakpoint()
                    self.pose2D_pub.publish(msg)
                    # print(f"{self.landmakr_update_count=}")
            else:
                self.landMark_detected = False

        self.landMark_detected = False
        return


def main(args=None):
    rclpy.init()
    node = landmarkPoseEstimation()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.destroy_node()
        rclpy.try_shutdown()
        exit()


if __name__ == "__main":
    main()


#   pose_msg = PoseWithCovarianceStamped()
#             ''' Set header '''
#             pose_msg.header.stamp = self.get_clock().now().to_msg()
#             pose_msg.header.frame_id = 'map'
#             ''' Set data '''
#             pose_msg.pose.pose.position.x = self.pose2D[0]
#             pose_msg.pose.pose.position.y = self.pose2D[1]
#             pose_msg.pose.pose.position.z = 0.0

#             pose_msg.pose.pose.orientation.x = 0.0
#             pose_msg.pose.pose.orientation.y = 0.0
#             pose_msg.pose.pose.orientation.z = 0.0
#             pose_msg.pose.pose.orientation.w = 1.0

#             pose_msg.pose.covariance = [1e-9, 0.0, 0.0, 0.0, 0.0, 0.0,
#                                         0.0, 1e9, 0.0, 0.0, 0.0, 0.0,
#                                         0.0, 0.0, 1000.0, 0.0, 0.0, 0.0,
#                                         0.0, 0.0, 0.0, 1000.0, 0.0, 0.0,
#                                         0.0, 0.0, 0.0, 0.0,1000.0, 0.0,
#                                         0.0, 0.0, 0.0, 0.0, 0.0, 1000.0]
