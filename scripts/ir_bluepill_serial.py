#! /usr/bin/env python3

import rclpy
import struct

from rclpy.node import Node 
from rclpy.qos import QoSReliabilityPolicy, QoSProfile
from std_msgs.msg import UInt16

from dev_pi_communicate.serial_comms import serial_comms

START_BYTE= 0b10100101
RECIEVE_SIZE = 4
TRANSMIT_SIZE = 0
serial_baudrate = 115200

ir_bluepill = '/dev/serial/by-id/usb-STMicroelectronics_STM32_Virtual_ComPort_00517C4B4D34-if00'
    
class IR_bluepill_node(Node):
    
    def __init__(self):

        super().__init__("IR_bluepill_node")
        self.serial_port = serial_comms(ir_bluepill, serial_baudrate, RECIEVE_SIZE, TRANSMIT_SIZE,"CRC")

        qos_profile = QoSProfile(depth= 10)
        qos_profile.reliability = QoSReliabilityPolicy.BEST_EFFORT
        
        self.ir_sensor_pub = self.create_publisher(UInt16, 'ir_sensor_data', qos_profile)
        self.timer1 = self.create_timer(0.001, self.serial_read_callback)
        # self.ball_stat = UInt16()

        self.get_logger().info("IR_bluepill_node ready...")
    
    def serial_read_callback(self):
            _data = self.serial_port.read_data()
            if _data == None:
                # print("Data none")
                return
            
            data_ = struct.unpack("H", _data[0:2])[0]

            ir_sensor_data = UInt16()
            ir_sensor_data.data = data_

            self.ir_sensor_pub.publish(ir_sensor_data)
            print(f"{hex(data_)}")

    
def main(args=None):
    rclpy.init()
    node = IR_bluepill_node()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt: 
        node.serial_port.close()
        node.destroy_node()
        rclpy.try_shutdown()
        exit()

if __name__ =='__main':
    main()
