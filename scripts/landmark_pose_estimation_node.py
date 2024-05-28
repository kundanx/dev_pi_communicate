#! /usr/bin/env python3

'''
ROS2 Node to publish 2d pose estimate to robot_localization package.
This node subscribes to /silo_number{published by apil} and /junction_type{published by linefollower node}
This node publishes 2D Pose whenever T_junction is detected.
2D pose is determined on the basis of which silo is the robot is navigating to.
'''
import os
import rclpy
import yaml
import math

from math import sin, cos
from rclpy.node import Node 
from rclpy.qos import QoSReliabilityPolicy, QoSProfile
from std_msgs.msg import UInt8
from std_msgs.msg import Float32MultiArray
from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseWithCovarianceStamped

'''
Junction euivalent Int ----------------------------
'''
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
'''----------------------------------------------'''

class landmarkPoseEstimation(Node):
    
    def __init__(self) -> None:

        super().__init__("landmark_pose_estimation_node")


        qos_profile = QoSProfile(depth= 10)
        qos_profile.reliability = QoSReliabilityPolicy.BEST_EFFORT

        self.odometry_subs = self.create_subscription(Odometry,"freewheel/global", self.odometry_callback,qos_profile)
        self.on_which_Area_sub = self.create_subscription( UInt8,"area_topic", self.area_callback,qos_profile )   
        self.siloNum_subs = self.create_subscription( UInt8,"silo_number", self.siloNum_subscriber_callback,qos_profile )   
        self.junctionType_subs = self.create_subscription( UInt8,"junction_type", self.junctionType_subscriber_callback,qos_profile ) 
        
        self.pose2D_timer = self.create_timer(0.01,self.landmark_updates)
        self.pose2D_pub = self.create_publisher(Float32MultiArray, 'landmark_pose', qos_profile)
         
        self.silo_number :UInt8 = 0
        self.pose2D = [0]*2
        self.seq_id = 1
        self.landMark_detected :bool = False
        self.is_on_silo_region :bool = False
        self.is_on_area3 : bool = False

        ''' Read YAML file '''
        file_path = os.path.join(os.path.dirname(__file__), '..', 'config/landmark_locations.yaml')
        with open(file_path, 'r') as stream:
            self.data_loaded = yaml.safe_load(stream)

        self.get_logger().info("landmark_pose_estimation_node ready...")

    def odometry_callback(self, msg:Odometry):
        if msg.pose.pose.position.x <= -1.3 :
            self.is_on_silo_region = True
        elif msg.pose.pose.position.x > -1.3:
            self.is_on_silo_region = False

      
    def area_callback(self, msg:UInt8):
        if msg.data == 0xA5:
            self.is_on_area3 = True
            self.get_logger().info("Map reset done...")
        # if( msg.data == 0xA5):
        #     pose_msg = PoseWithCovarianceStamped()
        #     ''' Set header '''
        #     pose_msg.header.stamp = self.get_clock().now().to_msg()
        #     pose_msg.header.frame_id = 'map'
        #     ''' Set data '''
        #     pose_msg.pose.pose.position.x = 0.0
        #     pose_msg.pose.pose.position.y = 0.0
        #     pose_msg.pose.pose.position.z = 0.0

        #     pose_msg.pose.pose.orientation.x = 0.0
        #     pose_msg.pose.pose.orientation.y = 0.0
        #     pose_msg.pose.pose.orientation.z = 0.0
        #     pose_msg.pose.pose.orientation.w = 1.0

        #     pose_msg.pose.covariance = [1e-9, 0.0, 0.0, 0.0, 0.0, 0.0,
        #                                 0.0, 1e-9, 0.0, 0.0, 0.0, 0.0,
        #                                 0.0, 0.0, 1e+9, 0.0, 0.0, 0.0,
        #                                 0.0, 0.0, 0.0, 1e+9, 0.0, 0.0,
        #                                 0.0, 0.0, 0.0, 0.0,1e+9, 0.0,
        #                                 0.0, 0.0, 0.0, 0.0, 0.0, 1e+9]
        #     self.pose2D_pub.publish(pose_msg)

    def siloNum_subscriber_callback(self,msg:UInt8) -> None:
        self.silo_number = msg.data
    
    def junctionType_subscriber_callback(self, msg:UInt8) -> None:
        if msg.data == T_JUNCTION:
            if self.silo_number == 1:
                self.pose2D = self.data_loaded['landmark_pose_estimation_node']['silo_1_TJunction']
                self.get_logger().info("sil0 1 T found")
    
            elif self.silo_number == 2:
                self.pose2D = self.data_loaded['landmark_pose_estimation_node']['silo_2_TJunction']
                self.get_logger().info("silo 2 T found")
            elif self.silo_number == 3:
                self.pose2D = self.data_loaded['landmark_pose_estimation_node']['silo_3_TJunction']
                self.get_logger().info("silo 3 T found")

            elif self.silo_number == 4:
                self.pose2D = self.data_loaded['landmark_pose_estimation_node']['silo_4_TJunction']
                self.get_logger().info("silo 4 T found")
    
            # if self.silo_number != 0:
            self.silo_number = 0
            self.landMark_detected = True

        elif msg.data == CROSS_JUNCTION:
            self.pose2D = self.data_loaded['landmark_pose_estimation_node']['cross_junction']
            self.get_logger().info("Cross Junc found")
            self.landMark_detected = True

        elif msg.data == L_JUNCTION or msg.data == RIGHT_TURN:
            if self.silo_number == 5:
                self.pose2D = self.data_loaded['landmark_pose_estimation_node']['silo_5_RJunction']
                self.get_logger().info("silo 5 T found")
                self.silo_number = 0
                self.landMark_detected = True

        elif msg.data == X_HORIZONTAL_LINE:
            self.pose2D = self.data_loaded['landmark_pose_estimation_node']['x_horizontal_line']
            self.landMark_detected = True
            self.get_logger().info("X_horizontal line found")

    def landmark_updates(self):
        if self.is_on_area3:
            if self.is_on_silo_region:         
                if self.landMark_detected: 
                    msg = Float32MultiArray()
                    msg.data[0] = self.pose2D[0]
                    msg.data[1] = self.pose2D[1]
                    self.pose2D_pub.publish(msg)
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

if __name__ =='__main':
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
