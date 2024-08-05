#! /usr/bin/env python3

import rclpy
import struct

from rclpy.node import Node 
from rclpy.qos import QoSReliabilityPolicy, QoSProfile

from std_msgs.msg import UInt16
from std_msgs.msg import UInt8

from dev_pi_communicate.serial_comms import serial_comms

START_BYTE= 0b10100101
RECIEVE_SIZE = 10
TRANSMIT_SIZE = 0
serial_baudrate = 115200

"""
Status Bit of Data to Represent No Update and Timeout   """
IR_LEFT_NO_UPDATE = 0x01
IR_RIGHT_NO_UPDATE = 0X02
TF_NO_UPDATE = 0x04
IR_LEFT_TIMEOUT = 0x08
IR_RIGHT_TIMEOUT = 0X10
TF_TIMEOUT = 0x20

sensor_bluepill_1 = '/dev/serial/by-id/usb-STMicroelectronics_STM32_Virtual_ComPort_4147395C3737-if00'
sensor_bluepill_2 = '/dev/serial/by-id/usb-STMicroelectronics_STM32_Virtual_ComPort_00517C4B4D34-if00'
sensor_bluepill = '/dev/serial/by-id/usb-STMicroelectronics_STM32_Virtual_ComPort_4D3A453D3030-if00'
    
class color_ir_tfmini_serial_node(Node):
    
    def __init__(self):

        super().__init__("color_ir_tfmini_serial_node")
        self.serial_port = serial_comms(sensor_bluepill, serial_baudrate, RECIEVE_SIZE, TRANSMIT_SIZE,"CRC")

        qos_profile = QoSProfile(depth= 10)
        qos_profile.reliability = QoSReliabilityPolicy.BEST_EFFORT
        
        self.ir_sensor_pub = self.create_publisher(UInt16, 'ir_sensor_data', qos_profile)
        self.inBall_status = self.create_publisher(UInt8, 'is_ball_inside', qos_profile)
        self.outBall_status = self.create_publisher(UInt8, 'is_only_ball', qos_profile)

        self.tfmini_pub = self.create_publisher(UInt16, 'tfmini_distance', qos_profile)

        self.timer1 = self.create_timer(0.001, self.serial_read_callback)

        self.ball_inside_detect_counter = 100
        self.only_ball_detect_counter = 100
        self.ball_inside_counter = 100
        self.only_ball_counter = 100

        self.get_logger().info("color_ir_tfmini_serial_node ready...")
    
    def serial_read_callback(self):
        _data = self.serial_port.read_data()
        if _data == None:
            # print("Data none")
            return
        """ Status, lf_ir, rt_ir, color_sensor, tf_dist, tf_strength """
        data = struct.unpack("BBBBHH", _data[0:8])

        ir_sensor_data = UInt16()

        if not (data[0] & IR_LEFT_TIMEOUT ):
            if not (data[0] & IR_RIGHT_TIMEOUT):
                ir_sensor_data.data = 0x00
                ir_sensor_data.data = ir_sensor_data.data |  int(data[2]) |  int(data[1] << 8)
                self.ir_sensor_pub.publish(ir_sensor_data)
            else:
                print(f"Right IR timeout")
        else:
            print(f"Left IR timeout")

        tf_distance = UInt16()

        if not ( data[0] & TF_TIMEOUT):
            tf_distance.data = data[4]
            self.tfmini_pub.publish(tf_distance)
        else:   
            print(f"TFmini timeout")

        in_ball_status = UInt8()
        out_ball_status = UInt8()
        
        byte = data[3]
        if (byte & 0x0f) == 0x0f:
            self.ball_inside_counter = 0
        
        # if  self.ball_inside_detect_counter >= 2:
        #     self.ball_inside_detect_counter = 0
        #     self.ball_inside_counter = 0
        
        if (byte & 0xf0) == 0xf0:
            self.only_ball_counter = 0
        
        # if  self.only_ball_detect_counter >= 2:
        #     self.only_ball_detect_counter = 0
        #     self.only_ball_counter = 0
        
        if self.ball_inside_counter < 50:
            self.ball_inside_counter += 1
            in_ball_status.data = 1
        else:
            in_ball_status.data = 0
        
        if self.only_ball_counter < 50:
            self.only_ball_counter +=1
            out_ball_status.data = 1
        else:
            out_ball_status.data = 0

        self.inBall_status.publish(in_ball_status)
        self.outBall_status.publish(out_ball_status)

        # print(f"{in_ball_status.data =}, {out_ball_status.data =}, {tf_distance.data=}, {bin(ir_sensor_data.data)=}")

    
def main(args=None):
    rclpy.init()
    node = color_ir_tfmini_serial_node()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt: 
        node.serial_port.close()
        node.destroy_node()
        rclpy.try_shutdown()
        exit()

if __name__ =='__main':
    main()
