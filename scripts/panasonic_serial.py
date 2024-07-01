#! /usr/bin/env python3

# -------------------------SERIAL BRIDGE BETWEEN RASP PI AND STM32-------------------------------
# This node subscribes to
#   I) 'cmd_robot'_vel topic to recieve velocity commands 
#   II) 'act_vel' from BT to recieve actuator control signals, and  write the data to stm discovery

# This node reads odometry value from bluepill and publish the data on
#   I) 'freewheel/odom' topic to ekf filter package through
#   II)'Ball_status' topic to BT

import rclpy
import struct
import serial
import time
import logging


from math import sin, cos
from rclpy.node import Node 
from rclpy.qos import QoSReliabilityPolicy, QoSProfile
from std_msgs.msg import UInt8

from dev_pi_communicate.crc8 import crc8

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

START_BYTE= 0b10100101
RECIEVE_SIZE = 3
TRANSMIT_SIZE = 0
serial_baudrate = 115200

serial_port_address_stm32 = '/dev/serial/by-id/usb-STM_Base_STM32_Virtual_ComPort_327130683331-if00'
serial_port_address_FTDI='/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A50285BI-if00-port0'
serial_port_address_black='/dev/serial/by-id/usb-1a86_USB2.0-Serial-if00-port0'
serial_port_bluepill ='/dev/serial/by-id/usb-STMicroelectronics_STM32_Virtual_ComPort_00517C4B4D34-if00'
    
class panasonic_serial(Node):
    
    def __init__(self):

        super().__init__("serial_bluepill")
        self.serial = serial.Serial(serial_port_address_stm32, serial_baudrate, timeout=1.0)
        self.rx_data_size = 1
        qos_profile = QoSProfile(depth= 10)
        qos_profile.reliability = QoSReliabilityPolicy.RELIABLE
        
        self.inBall_status = self.create_publisher(UInt8, 'is_ball_inside', qos_profile)
        self.outBall_status = self.create_publisher(UInt8, 'is_only_ball', qos_profile)
        self.timer1 = self.create_timer(0.01, self.serial_read_callback)
        self.ball_stat = UInt8()
        self.ball_inside_counter = 100
        self.only_ball_counter = 100

        self.get_logger().info("panasonic sensor ready...")
    
    def serial_read_callback(self):
            try:
                if self.serial.in_waiting < self.rx_data_size:
                    return
            except serial.SerialException as e:
                       
                # logger.error(f"Serial port error: {e}")
                self._reopen_serial_port()
                return

            except OSError as e:
                # logger.error(f"Serial port error: {e}")
                self._reopen_serial_port()
                return
            
            byte_ = self.serial.read(1)
            byte = struct.unpack("B", byte_)[0]

            in_ball_status = UInt8()
            out_ball_status = UInt8()

            if byte & 0x0f == 0x0f:
                self.ball_inside_counter = 0
            
            if byte & 0xf0 == 0xf0:
                self.only_ball_counter = 0
            
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
            # print(f"{hex(byte)}")
        #    print(f"{self.ball_stat.data =}")

    def _reopen_serial_port(self):
        try:
            time.sleep(2)     
            self.serial.close()
            self.serial = serial.Serial(serial_port_address_stm32, serial_baudrate, timeout=1.0)
            logger.info("Serial port reopened successfully")

        except serial.SerialException as e:
            logger.error(f"Failed to reopen serial port: {e}")
        except OSError as e:
            logger.error(f"OSErorr::Failed to reopen serial port: {e}")
        except Exception as e:
            logger.error(f"Serial port unknown error: {e}")
           
    def calculate_checksum(self , data = []):
        digest = int()
        for i in range(1,len(data)):
            digest += data[i]
        return int(digest)
    
    def calculate_crc(self, data=[]):
        hash_func=crc8()
        hash_func.update(data)
        return hash_func.digest()[0]
    
def main(args=None):
    rclpy.init()
    node = panasonic_serial()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt: 
        node.serial_port.close()
        node.destroy_node()
        rclpy.try_shutdown()
        exit()

if __name__ =='__main':
    main()
