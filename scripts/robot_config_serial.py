#! /usr/bin/env python3

import rclpy
import struct
import serial
import time
import logging
from enum import Enum


from math import sin, cos
from rclpy.node import Node 
from rclpy.qos import QoSReliabilityPolicy, QoSProfile
from std_msgs.msg import UInt8
from std_msgs.msg import Int8

from dev_pi_communicate.crc8 import crc8

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

START_BYTE = 0xA5
RECIEVE_SIZE = 1
TRANSMIT_SIZE = 1
serial_baudrate = 115200

serial_port_pico = '/dev/serial/by-id/usb-Raspberry_Pi_Pico_E6611CB71F34112A-if00'

"""
  Recieve data:
    B7: Red/Blue team_color
    B6: Start/Retry Zone
    B5: Start signal
    B5: Wait signal
    0000

  Transmit data: 
    B7: Red 
    B6: Blue 
    00 0000
"""

RED = 1
BLUE = -1

START_ZONE = 1
RETRY_ZONE = 2

START = 0x0f
WAIT = 0xf0
    
class robot_config_serial(Node):
    
    def __init__(self):

        super().__init__("robot_config_serial")
        self.serial = serial.Serial(serial_port_pico, serial_baudrate, timeout=1.0)
        self.rx_data_size = 1
        qos_profile = QoSProfile(depth= 10)
        qos_profile.reliability = QoSReliabilityPolicy.BEST_EFFORT
        
        self.team_color_pub = self.create_publisher(Int8, 'team_color', qos_profile)
        self.zone_pub = self.create_publisher(UInt8, 'zone_status', qos_profile)
        self.start_wait_pub = self.create_publisher(UInt8, 'go_or_wait', qos_profile)

        self.team_color = UInt8()

        self.timer1 = self.create_timer(0.001, self.serial_read_callback)
        self.get_logger().info("robot_config_serial ready...")
    
    def serial_read_callback(self):
            try:
                if self.serial.in_waiting < 1:
                    return
            except serial.SerialException as e:
                logger.error(f"Serial port error: {e}")
                self._reopen_serial_port()
                return

            except OSError as e:
                logger.error(f"Serial port error: {e}")
                self._reopen_serial_port()
                return
            
            start_byte_ = self.serial.read(1)
            if int.from_bytes(start_byte_, 'big') != START_BYTE:
                print("Start byte not matched")
                return

            byte_ = self.serial.read(1)
            byte = struct.unpack("B", byte_)[0]

            if byte == 0b11111111:
                byte = 0x00

            teamcolor = Int8()
            if byte & 0b10000000:  
                teamcolor.data = RED
            else:
                teamcolor.data = BLUE
            
            zone = UInt8()
            if byte & 0b01000000:
                zone.data = START_ZONE
            else:
                zone.data = RETRY_ZONE
            
            start_or_wait = UInt8()
            if (byte & 0b00100000) :
                start_or_wait.data = START
            elif (byte & 0b00010000):
                start_or_wait.data = WAIT
            else:
                start_or_wait.data = 0x00

            self.team_color_pub.publish(teamcolor)
            self.zone_pub.publish(zone)
            self.start_wait_pub.publish(start_or_wait)

            self.serial_transmit_callback()
            # print(f"{bin(byte)}")
            # print(f"team_color: {teamcolor.data}, zone: {zone.data}, start_wait: {hex(start_or_wait.data)}")
    
    def serial_transmit_callback(self):
        self.team_color.data = 0b01000000
        data = bytes(struct.pack("B", self.team_color.data))
        # data = b"".join(data)

        self.serial.write(data)
        self.serial.reset_output_buffer()


    

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
    node = robot_config_serial()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt: 
        node.serial_port.close()
        node.destroy_node()
        rclpy.try_shutdown()
        exit()

if __name__ =='__main':
    main()
