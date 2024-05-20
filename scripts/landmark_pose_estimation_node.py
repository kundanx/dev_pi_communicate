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

from math import sin, cos
from rclpy.node import Node 
from std_msgs.msg import UInt8
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
        
        self.siloNum_subs = self.create_subscription( UInt8,"silo_number", self.siloNum_subscriber_callback,10 )   
        self.junctionType_subs = self.create_subscription( UInt8,"junction_type", self.junctionType_subscriber_callback,10 ) 
        self.pose2D_pub = self.create_publisher(PoseWithCovarianceStamped, 'landmark/pose', 10)
         
        self.silo_number :UInt8 = 0
        self.pose2D = [0]*2
        self.seq_id = 1
        self.landMark_detected :bool = False
        ''' Read YAML file '''
        file_path = os.path.join(os.path.dirname(__file__), '..', 'config/landmark_locations.yaml')
        with open(file_path, 'r') as stream:
            self.data_loaded = yaml.safe_load(stream)

        self.get_logger().info("landmark_pose_estimation_node ready...")

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
            #     self.silo_number = 0
            self.landMark_detected = True

        elif msg.data == CROSS_JUNCTION:
            self.pose2D = self.data_loaded['landmark_pose_estimation_node']['cross_junction']
            self.get_logger().info("Cross Junc found")
            self.landMark_detected = True
        elif msg.data == L_JUNCTION or msg.data == RIGHT_TURN:
            if self.silo_number == 5:
                self.pose2D = self.data_loaded['landmark_pose_estimation_node']['silo_5_RJunction']
                self.get_logger().info("silo 5 T found")
                self.landMark_detected = True
        elif msg.data == X_HORIZONTAL_LINE:
            self.pose2D = self.data_loaded['landmark_pose_estimation_node']['x_horizontal_line']
            self.landMark_detected = False
            pose_msg = PoseWithCovarianceStamped()
            ''' Set header '''
            pose_msg.header.stamp = self.get_clock().now().to_msg()
            pose_msg.header.frame_id = 'map'
            ''' Set data '''
            pose_msg.pose.pose.position.x = self.pose2D[0]
            pose_msg.pose.pose.position.y = self.pose2D[1]
            pose_msg.pose.pose.position.z = 0.0

            pose_msg.pose.pose.orientation.x = 0.0
            pose_msg.pose.pose.orientation.y = 0.0
            pose_msg.pose.pose.orientation.z = 0.0
            pose_msg.pose.pose.orientation.w = 1.0

            pose_msg.pose.covariance = [1e-9, 0.0, 0.0, 0.0, 0.0, 0.0,
                                        0.0, 1e9, 0.0, 0.0, 0.0, 0.0,
                                        0.0, 0.0, 1000.0, 0.0, 0.0, 0.0,
                                        0.0, 0.0, 0.0, 1000.0, 0.0, 0.0,
                                        0.0, 0.0, 0.0, 0.0,1000.0, 0.0,
                                        0.0, 0.0, 0.0, 0.0, 0.0, 1000.0]
            self.pose2D_pub.publish(pose_msg)
            self.get_logger().info("X_horizontal line found")


        if self.landMark_detected :
                self.landMark_detected = False
                pose_msg = PoseWithCovarianceStamped()
                ''' Set header '''
                pose_msg.header.stamp = self.get_clock().now().to_msg()
                pose_msg.header.frame_id = 'map'
                ''' Set data '''
                pose_msg.pose.pose.position.x = self.pose2D[0]
                pose_msg.pose.pose.position.y = self.pose2D[1]
                pose_msg.pose.pose.position.z = 0.0

                pose_msg.pose.pose.orientation.x = 0.0
                pose_msg.pose.pose.orientation.y = 0.0
                pose_msg.pose.pose.orientation.z = 0.0
                pose_msg.pose.pose.orientation.w = 1.0

                pose_msg.pose.covariance = [1e-9, 0.0, 0.0, 0.0, 0.0, 0.0,
                                            0.0, 1e-9, 0.0, 0.0, 0.0, 0.0,
                                            0.0, 0.0, 0.001, 0.0, 0.0, 0.0,
                                            0.0, 0.0, 0.0, 0.01, 0.0, 0.0,
                                            0.0, 0.0, 0.0, 0.0, 0.001, 0.0,
                                            0.0, 0.0, 0.0, 0.0, 0.0, 0.001]
                self.pose2D_pub.publish(pose_msg)

    
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
