# #! /usr/bin/env python3

# # This node recieves imu data from pico serially and publishes to ekf filter package

import rclpy
import serial
import struct
import time
from math import sin, cos, atan2, sqrt,  pi

from rclpy.node import Node 
from sensor_msgs.msg import Imu

from dev_pi_communicate.crc8 import crc8
from dev_pi_communicate.serial_comm import serial_comms

START_BYTE = 0xA5
serial_baudrate = 115200
pico_address='/dev/serial/by-id/usb-Raspberry_Pi_Pico_E6611CB71F34112A-if00'
esp_address='/dev/serial/by-id/usb-Silicon_Labs_CP2102_USB_to_UART_Bridge_Controller_0001-if00-port0'
rx_data_size = 42
sum = 0

class ImuNode(Node):
    def __init__(self):
        super().__init__("imu_node")
        #  Odom data publisher
        self.imu_publisher = self.create_publisher(Imu, 'imu/data', 10)
        self.usb_port = serial_comms(esp_address, serial_baudrate,rx_data_size)
        
        self.serial_port = serial.Serial(esp_address, serial_baudrate)
        self.data = [float(1), float(0), float(0), float(0), float(0), float(0), float(0), float(0), float(0), float(0)]
        # self.is_waiting_for_start_byte = True
        self.last_publish_time = time.time()
        self.get_logger().info("Recieving imu data")
        
    # Read callback function
    # def serial_receive(self):
    #     if self.serial_port.in_waiting < rx_data_size:
    #         return
    
    #     if self.is_waiting_for_start_byte:
    #         byte = self.serial_port.read(1)
    #         if int.from_bytes(byte, 'big') == START_BYTE:
    #             # print(byte)
    #             self.is_waiting_for_start_byte = False
    #         else:
    #             # pass
    #             self.get_logger().info("Start Byte Not Matched")
    #     else:
    #         self.is_waiting_for_start_byte = True
    #         data_str = self.serial_port.read(rx_data_size-1)
    #         hash = self.calc_crc(data_str[:-1])
    #         if hash == data_str[-1]:
    #             # self.serial_port.reset_input_buffer()
    #             self.data = struct.unpack("ffffffffff", data_str[0:-1])
    #             self.process_data()
    #         else:
    #             # pass
    #             self.get_logger().info(data_str)
    
    def serial_read_callback(self):

        _data = self.usb_port.read_data()
        print(_data)
        if _data == None:
            return 
        if (time.time() - self.last_publish_time >= 0.03):
            
            self.data[0], self.data[1], self.data[2], self.data[3], self.data[4], self.data[5], self.data[6], self.data[7], self.data[8], self.data[9] , hash = struct.unpack("ddddddddddc", _data)
            imu_msg = Imu()
            #  Assign header values to the imu_msg
            imu_msg.header.stamp=self.get_clock().now().to_msg()
            imu_msg.header.frame_id="base_link"

            # Assign actuall values to the imu_msg
            imu_msg.orientation.w = self.data[0]
            imu_msg.orientation.x = self.data[1]
            imu_msg.orientation.y = self.data[2]
            imu_msg.orientation.z = self.data[3]

            imu_msg.angular_velocity.x = self.data[4]
            imu_msg.angular_velocity.y = self.data[5]
            imu_msg.angular_velocity.z = self.data[6]

            imu_msg.linear_acceleration.x = self.data[7]
            imu_msg.linear_acceleration.y = self.data[8]
            imu_msg.linear_acceleration.z = self.data[9]

            imu_msg.orientation_covariance[0] = 0.00121847
            imu_msg.orientation_covariance[1] = 0.0
            imu_msg.orientation_covariance[2] = 0.0
            imu_msg.orientation_covariance[3] = 0.0
            imu_msg.orientation_covariance[4] = 0.00121847
            imu_msg.orientation_covariance[5] = 0.0
            imu_msg.orientation_covariance[6] = 0.0
            imu_msg.orientation_covariance[7] = 0.0
            imu_msg.orientation_covariance[8] = 0.00121847

            imu_msg.angular_velocity_covariance[0] = 4.4944
            imu_msg.angular_velocity_covariance[1] = 0.0
            imu_msg.angular_velocity_covariance[2] = 0.0
            imu_msg.angular_velocity_covariance[3] = 0.0
            imu_msg.angular_velocity_covariance[4] = 4.4944
            imu_msg.angular_velocity_covariance[5] = 0.0
            imu_msg.angular_velocity_covariance[6] = 0.0
            imu_msg.angular_velocity_covariance[7] = 0.0
            imu_msg.angular_velocity_covariance[8] = 4.4944

            imu_msg.linear_acceleration_covariance[0] = 0.25
            imu_msg.linear_acceleration_covariance[1] = 0.0
            imu_msg.linear_acceleration_covariance[2] = 0.0
            imu_msg.linear_acceleration_covariance[3] = 0.0
            imu_msg.linear_acceleration_covariance[4] = 0.25
            imu_msg.linear_acceleration_covariance[5] = 0.0
            imu_msg.linear_acceleration_covariance[6] = 0.0
            imu_msg.linear_acceleration_covariance[7] = 0.0
            imu_msg.linear_acceleration_covariance[8] = 0.25

            # Publish message
            self.imu_publisher.publish(imu_msg)
            self.last_publish_time = time.time()

            yaw, pitch, roll = quaternion_to_yawpitchroll(self.data[0], self.data[1], self.data[2], self.data[3])
            self.get_logger().info('ypr: "%f %f %f"' %(yaw*180/pi, pitch*180/pi, roll*180/pi))

    def calc_crc(self, data=[]):
        hash_func = crc8()
        hash_func.update(data)
        return hash_func.digest()[0]

    def calc_checksum(self, data=[]):
        checksum = 0
        for i in range(0, len(data)):
            checksum = checksum ^ data[i]
        return checksum
    
def angleChange(curr, prev):
    change = 0
    if (prev > pi/2) and (curr < -pi/2):
        change = (pi - prev) + (pi + curr)
    elif (prev < -pi/2) and (curr > pi/2):
        change = -(pi + prev) - (pi - curr)
    else:
        change = curr - prev
    return change

        
def yawpitchroll_to_quaternion(yaw, pitch, roll):
    cr = cos(roll * 0.5)
    sr = sin(roll * 0.5)
    cp = cos(pitch * 0.5)
    sp = sin(pitch * 0.5)
    cy = cos(yaw * 0.5)
    sy = sin(yaw * 0.5)

    qw = cr * cp * cy + sr * sp * sy
    qx = sr * cp * cy - cr * sp * sy
    qy = cr * sp * cy + sr * cp * sy
    qz = cr * cp * sy - sr * sp * cy

    return qw, qx, qy, qz

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

def main(args=None):
    rclpy.init()
    imu_node = ImuNode()
    while True:
        try:
            imu_node.serial_read_callback()
        except KeyboardInterrupt:  
            imu_node.serial_port.close()
            imu_node.destroy_node()
            rclpy.try_shutdown()
            exit()
   
if __name__ =='__main__':
    main()




# This node recieves imu data from pico serially and publishes to ekf filter package

# import rclpy
# import serial
# import struct
# import time
# from math import sin, cos, atan2, sqrt,  pi
# from rclpy.node import Node 
# from dev_pi_communicate.crc8 import crc8
# from sensor_msgs.msg import Imu

# START_BYTE = 0xA5
# serial_baudrate = 115200
# pico_address='/dev/serial/by-id/usb-Raspberry_Pi_Pico_E6611CB71F34112A-if00'
# esp_address='/dev/serial/by-id/usb-Silicon_Labs_CP2102_USB_to_UART_Bridge_Controller_0001-if00-port0'
# rx_data_size = 42
# sum = 0

# class ImuNode(Node):
#     def __init__(self):
#         super().__init__("imu_node")
#         #  Odom data publisher
#         self.imu_publisher = self.create_publisher(Imu, 'imu/data', 10)
#         self.serial_port = serial.Serial(esp_address, serial_baudrate)
#         self.data = [float(1), float(0), float(0), float(0), float(0), float(0), float(0), float(0), float(0), float(0)]
#         self.is_waiting_for_start_byte = True
#         self.last_publish_time = time.time()
#         self.get_logger().info("Recieving imu data")
        
#     # Read callback function
#     def serial_receive(self):
#         if self.serial_port.in_waiting < rx_data_size:
#             return
    
#         if self.is_waiting_for_start_byte:
#             byte = self.serial_port.read(1)
#             if int.from_bytes(byte, 'big') == START_BYTE:
#                 # print(byte)
#                 self.is_waiting_for_start_byte = False
#             else:
#                 # pass
#                 self.get_logger().info("Start Byte Not Matched")
#         else:
#             self.is_waiting_for_start_byte = True
#             data_str = self.serial_port.read(rx_data_size-1)
#             hash = self.calc_crc(data_str[:-1])
#             if hash == data_str[-1]:
#                 # self.serial_port.reset_input_buffer()
#                 self.data = struct.unpack("ffffffffff", data_str[0:-1])
#                 self.process_data()
#             else:
#                 # pass
#                 self.get_logger().info(data_str)
    
#     def process_data(self):
#         now = time.time()
#         if now - self.last_publish_time < 0.04:
#             return
        
#         imu_msg = Imu()
#         #  Assign header values to the imu_msg
#         imu_msg.header.stamp=self.get_clock().now().to_msg()
#         imu_msg.header.frame_id="base_link"

#         # Assign actuall values to the imu_msg
#         imu_msg.orientation.w = self.data[0]
#         imu_msg.orientation.x = self.data[1]
#         imu_msg.orientation.y = self.data[2]
#         imu_msg.orientation.z = self.data[3]

#         imu_msg.angular_velocity.x = self.data[4]
#         imu_msg.angular_velocity.y = self.data[5]
#         imu_msg.angular_velocity.z = self.data[6]

#         imu_msg.linear_acceleration.x = self.data[7]
#         imu_msg.linear_acceleration.y = self.data[8]
#         imu_msg.linear_acceleration.z = self.data[9]

#         imu_msg.orientation_covariance[0] = 0.00121847
#         imu_msg.orientation_covariance[1] = 0.0
#         imu_msg.orientation_covariance[2] = 0.0
#         imu_msg.orientation_covariance[3] = 0.0
#         imu_msg.orientation_covariance[4] = 0.00121847
#         imu_msg.orientation_covariance[5] = 0.0
#         imu_msg.orientation_covariance[6] = 0.0
#         imu_msg.orientation_covariance[7] = 0.0
#         imu_msg.orientation_covariance[8] = 0.00121847

#         imu_msg.angular_velocity_covariance[0] = 4.4944
#         imu_msg.angular_velocity_covariance[1] = 0.0
#         imu_msg.angular_velocity_covariance[2] = 0.0
#         imu_msg.angular_velocity_covariance[3] = 0.0
#         imu_msg.angular_velocity_covariance[4] = 4.4944
#         imu_msg.angular_velocity_covariance[5] = 0.0
#         imu_msg.angular_velocity_covariance[6] = 0.0
#         imu_msg.angular_velocity_covariance[7] = 0.0
#         imu_msg.angular_velocity_covariance[8] = 4.4944

#         imu_msg.linear_acceleration_covariance[0] = 0.25
#         imu_msg.linear_acceleration_covariance[1] = 0.0
#         imu_msg.linear_acceleration_covariance[2] = 0.0
#         imu_msg.linear_acceleration_covariance[3] = 0.0
#         imu_msg.linear_acceleration_covariance[4] = 0.25
#         imu_msg.linear_acceleration_covariance[5] = 0.0
#         imu_msg.linear_acceleration_covariance[6] = 0.0
#         imu_msg.linear_acceleration_covariance[7] = 0.0
#         imu_msg.linear_acceleration_covariance[8] = 0.25

#         # Publish message
#         self.imu_publisher.publish(imu_msg)
#         self.last_publish_time = now

#         yaw, pitch, roll = quaternion_to_yawpitchroll(self.data[0], self.data[1], self.data[2], self.data[3])
#         self.get_logger().info('ypr: "%f %f %f"' %(yaw*180/pi, pitch*180/pi, roll*180/pi))

#     def calc_crc(self, data=[]):
#         hash_func = crc8()
#         hash_func.update(data)
#         return hash_func.digest()[0]

#     def calc_checksum(self, data=[]):
#         checksum = 0
#         for i in range(0, len(data)):
#             checksum = checksum ^ data[i]
#         return checksum
    
# def angleChange(curr, prev):
#     change = 0
#     if (prev > pi/2) and (curr < -pi/2):
#         change = (pi - prev) + (pi + curr)
#     elif (prev < -pi/2) and (curr > pi/2):
#         change = -(pi + prev) - (pi - curr)
#     else:
#         change = curr - prev
#     return change

        
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
#     imu_node = ImuNode()
#     while True:
#         try:
#             imu_node.serial_receive()
#         except KeyboardInterrupt:  
#             imu_node.serial_port.close()
#             imu_node.destroy_node()
#             rclpy.try_shutdown()
#             exit()
   
# if __name__ =='__main__':
#     main()