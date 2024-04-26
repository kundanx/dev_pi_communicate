#! /usr/bin/env python3
import math
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from nav_msgs.msg import Odometry
from sensor_msgs.msg import Imu

class subscriber(Node):
    def __init__(self):
        super().__init__("subscriber_node")
        self.subscriber_to_filter_node = self.create_subscription(Odometry, "/odometry/filtered", self.recieve_callback_filter, 10)
        # self.subscriber_to_imu_node = self.create_subscription (Imu, "/imu/data", self.recieve_callback_imu, 10)
        self.subscriber_to_freewheel_node = self.create_subscription(Odometry, "/freewheel/odom", self.recieve_callback_freewheel, 10)
        self.yaw = [0.0]*3
        self.get_logger().info("Quaternion to RollPitchYaw....")
    
    def recieve_callback_filter(self, msg:Odometry):
        q =[msg.pose.pose.orientation.x,
            msg.pose.pose.orientation.y,
            msg.pose.pose.orientation.z,
            msg.pose.pose.orientation.w]
        
        rpy= self.quaternon_to_rollpitchyaw(q)
        self.yaw[2] = rpy[2]*180/math.pi
    
    def recieve_callback_imu(self, msg:Imu):
        q =[msg.orientation.x,
            msg.orientation.y,
            msg.orientation.z,
            msg.orientation.w]
        
        rpy= self.quaternon_to_rollpitchyaw(q)
        self.yaw[0]= rpy[2]*180/math.pi
        # self.get_logger().info(f"yaw from Imu: {self.yaw[0]}")
    
    def recieve_callback_freewheel(self, msg:Odometry):
        x = msg.pose.pose.position.x
        y = msg.pose.pose.position.y
        z = msg.pose.pose.position.z

        q =[msg.pose.pose.orientation.x,
            msg.pose.pose.orientation.y,
            msg.pose.pose.orientation.z,
            msg.pose.pose.orientation.w]
        
        rpy= self.quaternon_to_rollpitchyaw(q)
        self.yaw[1]= rpy[2]*180/math.pi
        self.get_logger().info(f"x:{x},  y:{y},  z:{z},  yaw_filter:{self.yaw[2]},  yaw_Freewheel:{self.yaw[1]}")
        # self.get_logger().info(f"")
    
    def quaternon_to_rollpitchyaw(self,q):

        # roll (x-axis rotation)
        sinr_cosp = 2 * (q[3] * q[0] + q[1] * q[2])
        cosr_cosp = 1 - 2 * (q[0] * q[0] + q[1] * q[1])
        roll = math.atan2(sinr_cosp, cosr_cosp)

        # pitch (y-axis rotation)
        sinp = math.sqrt(1 + 2 * (q[3] * q[1] - q[0] * q[2]))
        cosp = math.sqrt(1 - 2 * (q[3] * q[1] - q[0] * q[2]))
        pitch = 2 * math.atan2(sinp, cosp) -math.pi / 2 

        #  yaw (z-axis rotation)
        siny_cosp = 2 * (q[3] * q[2] + q[0] * q[1])
        cosy_cosp = 1 - 2 * (q[1] * q[1] + q[2] * q[2])
        yaw = math.atan2(siny_cosp, cosy_cosp)

        return roll, pitch, yaw

def main(args=None):
    rclpy.init()
    node = subscriber()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ ==' __main__':
    main()


# import rclpy
# from math import sin, cos, atan2, sqrt,  pi
# from rclpy.node import Node
# from nav_msgs.msg import Odometry
# from std_msgs.msg import Int32MultiArray
# from geometry_msgs.msg import Twist

# class OdomSubNode(Node):
#     def __init__(self):
#         super().__init__("odom_subscriber_node")
#         self.imu_subscriber = self.create_subscription(Odometry, '/odometry/filtered', self.process_data, 10)
        
#     def process_data(self, odom_msg):
#         x = odom_msg.pose.pose.position.x
#         y = odom_msg.pose.pose.position.y
#         z = odom_msg.pose.pose.position.z

#         yaw, pitch, roll = quaternion_to_yawpitchroll(odom_msg.pose.pose.orientation.w,
#                                                       odom_msg.pose.pose.orientation.x,
#                                                       odom_msg.pose.pose.orientation.y,
#                                                       odom_msg.pose.pose.orientation.z)
        

#         self.get_logger().info('xyz:"%f %f %f" ypr: "%f %f %f"' %(x, y, z, yaw*180/pi, pitch*180/pi, roll*180/pi))

        
# def yawpitchroll_to_quaternion(yaw, pitch, roll):
#     cr = cos(roll * 0.5)
#     sr = sin(roll * 0.5)
#     cp = cos(pitch * 0.5)
#     sp = sin(pitch * 0.5)
#     cy = cos(yaw * 0.5)
#     sy = sin(yaw * 0.5)

#     qw = cr * cp * cy + sr * sp * sy
#     qx = sr * cp * cy - cr * sp * sy
#     qy = cr * sp * cy + sr * cp * sy
#     qz = cr * cp * sy - sr * sp * cy

#     return qw, qx, qy, qz

# def quaternion_to_yawpitchroll(w, x, y, z):
#     # roll (x-axis rotation)
#     sinr_cosp = 2 * (w * x + y * z)
#     cosr_cosp = 1 - 2 * (x * x + y * y)
#     roll = atan2(sinr_cosp, cosr_cosp)

#     # pitch (y-axis rotation)
#     sinp = sqrt(1 + 2 * (w * y - x * z))
#     cosp = sqrt(1 - 2 * (w * y - x * z))
#     pitch = 2 * atan2(sinp, cosp) - pi / 2

#     # yaw (z-axis rotation)
#     siny_cosp = 2 * (w * z + x * y)
#     cosy_cosp = 1 - 2 * (y * y + z * z)
#     yaw = atan2(siny_cosp, cosy_cosp)

#     return  yaw, pitch, roll

# def main(args=None):
#     rclpy.init()
#     odom_node = OdomSubNode()
#     try:
#         rclpy.spin(odom_node)
#     except KeyboardInterrupt:
#         odom_node.destroy_node()
#         rclpy.try_shutdown()
#         exit()
   
# if __name__ =='__main__':
#     main()