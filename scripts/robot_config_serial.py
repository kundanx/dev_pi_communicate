#! /usr/bin/env python3

import logging
import os
import struct
import time
from enum import Enum
from math import cos, sin

import rclpy
import serial
import yaml
from rclpy.node import Node
from rclpy.qos import QoSProfile, QoSReliabilityPolicy
from std_msgs.msg import Int8, UInt8

from dev_pi_communicate.crc8 import crc8

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

START_BYTE = 0xA5
RECIEVE_SIZE = 1
TRANSMIT_SIZE = 1
serial_baudrate = 115200

serial_port_pico_ = "/dev/serial/by-id/usb-Raspberry_Pi_Pico_E6611CB71F34112A-if00"
serial_port_pico__= "/dev/serial/by-id/usb-Raspberry_Pi_Pico_E6614103E74E4E36-if00"
serial_port_pico = "/dev/serial/by-id/usb-Raspberry_Pi_Pico_E661AC886355C027-if00"


"""
  Recieve data:
    B7: Blue/RED team_color
    B6: Start/Retry Zone
    B5: Start signal
    B4: Wait signal
    0000

  Transmit data: 
    B7: Red 
    B6: Blue 
    00 0000
"""

BLUE = 1
RED = -1

BLUE_ = 0b01000000
RED_ = 0b10000000
GREEN_ = 0b00000000

START_ZONE = 1
RETRY_ZONE = 2

START = 0x0F
WAIT = 0xF0


class robot_config_serial(Node):
    def __init__(self):
        super().__init__("robot_config_serial")
        self.serial = serial.Serial(serial_port_pico, serial_baudrate, timeout=1.0)
        self.rx_data_size = 1
        qos_profile = QoSProfile(depth=10)
        qos_profile.reliability = QoSReliabilityPolicy.BEST_EFFORT

        ## Config file for Apil
        self.robot_config_file = "/home/apil/main_ws/src/robot/config/common.yaml"
        with open(self.robot_config_file, "r") as file:
            self.yaml_data = yaml.safe_load(file)
        self.write_config = True

        self.team_color_pub = self.create_publisher(Int8, "team_color", qos_profile)
        self.zone_pub = self.create_publisher(UInt8, "zone_status", qos_profile)
        self.start_wait_pub = self.create_publisher(UInt8, "go_or_wait", qos_profile)

        self.team_color_linefollow_subs = self.create_subscription(
            Int8, "color_feedback/linefollow", self.line_follow, qos_profile
        )

        self.team_color_GoToBall_subs = self.create_subscription(
            Int8, "color_feedback/GoToBallPose", self.GoToBall, qos_profile
        )

        self.team_color_GoToSilo_subs = self.create_subscription(
            Int8, "color_feedback/GoToSiloPose", self.GoToSilo, qos_profile
        )

        self.team_color_GoToOrigin_subs = self.create_subscription(
            Int8, "color_feedback/GoToOrigin", self.GoToOrigin, qos_profile
        )

        self.team_color_GoToMiddle_subs = self.create_subscription(
            Int8, "color_feedback/GoToMiddle", self.GoToMiddle, qos_profile
        )

        self.team_color_Recovery_subs = self.create_subscription(
            Int8, "color_feedback/RecoveryNode", self.RecoveryNode, qos_profile
        )

        self.aligned_silo_subs = self.create_subscription(
            UInt8, "aligned_silo", self.silo_number_callback, 10
        )
        
        self.aligned_silo = UInt8()
        self.lf_color: int = 0
        self.ballPose_color: int = 0
        self.origin_color: int = 0
        self.middle_color: int = 0
        self.silo_color: int = 0
        self.recovery_color: int = 0

        self.lf_last_rx: int = 0
        self.ballPose_last_rx: int = 0
        self.origin_last_rx: int = 0
        self.middle_last_rx: int = 0
        self.silo_last_rx: int = 0
        self.recovery_last_rx: int = 0

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
        if int.from_bytes(start_byte_, "big") != START_BYTE:
            print("Start byte not matched")
            return

        byte_ = self.serial.read(1)
        byte = struct.unpack("B", byte_)[0]

        if byte == 0b11111111:
            byte = 0x00

        """ Team color """
        config_team = ""
        teamcolor = Int8()
        if byte & 0b10000000:
            teamcolor.data = BLUE
            config_team = "blue"
        else:
            teamcolor.data = RED
            config_team = "red"

        # teamcolor.data = BLUE
        # config_team = "blue"

        # teamcolor.data = RED
        # config_team = "red"

        if self.write_config:
            self.yaml_data["/**"]["ros__parameters"]["team_color"] = config_team
            with open(self.robot_config_file, "w") as file:
                yaml.safe_dump(self.yaml_data, file)
            self.write_config = False

        """ Zone """
        zone = UInt8()
        if byte & 0b01000000:
            zone.data = START_ZONE
        else:
            zone.data = RETRY_ZONE
        
        # zone.data = START_ZONE


        """ Start Wait """
        start_or_wait = UInt8()
        if byte & 0b00100000:
            start_or_wait.data = START
        elif byte & 0b00010000:
            start_or_wait.data = WAIT
        else:
            start_or_wait.data = 0x00

        # start_or_wait.data = START
        

        self.team_color_pub.publish(teamcolor)
        self.zone_pub.publish(zone)
        self.start_wait_pub.publish(start_or_wait)

        self.serial_transmit_callback()

        # print(f"team_color: {teamcolor.data}, zone: {zone.data}, start_wait: {hex(start_or_wait.data)}")

    def serial_transmit_callback(self):
        # self.team_color = UInt8()
        transmit_data = UInt8()

        now = time.time() * 1000
        if now - self.lf_last_rx > 100:
            self.lf_color = 0
            print("ERROR: Linefollow node")

        if now - self.ballPose_last_rx > 100:
            self.ballPose_color = 0
            print("ERROR: GoToBallPose node")

        if now - self.silo_last_rx > 100:
            self.silo_color = 0
            print("ERROR: GoToSiloPose node")

        if now - self.origin_last_rx > 100:
            self.origin_color = 0
            print("ERROR: GoToOrigin node")
# 
        if now - self.middle_last_rx > 100:
            self.middle_color = 0
            print("ERROR: GoToMiddle node")

        if now - self.recovery_last_rx > 100:
            self.recovery_color = 0
            print("ERROR: RecoveryNode node")

        """
          0x01 = Green + Blue
          0x02 = Green + Red
          0x03 = Blue + Red
          0x04 = Green + Blue + Red
          0x05 = Green
          0x06 = Red
          0x07 = Blue
          0x08 = Green
        """

        if (
            self.lf_color
            & self.silo_color
            & self.middle_color 
            & self.ballPose_color
            & self.recovery_color
        ) == -1:
            # Team color = RED
            transmit_data.data = 0x06
        elif (
            self.lf_color
            & self.silo_color
            & self.middle_color 
            & self.ballPose_color
            & self.recovery_color
        ) == 1:
            # Team color = BLUE
            transmit_data.data = 0x07

        else:
            # Nodes not ready yet, color = GREEN
            transmit_data.data = 0x08
        

        if self.aligned_silo.data != 0x00:
            transmit_data.data = self.aligned_silo.data
        

        data = bytes(struct.pack("B", transmit_data.data))
        # print(f"{transmit_data.data = }")
        # data = b"".join(data)
        # print(f"{data = }")

        self.serial.write(data)
        self.serial.reset_output_buffer()

    def line_follow(self, msg: Int8):
        self.lf_color = msg.data
        self.lf_last_rx = time.time() * 1000

    def GoToBall(self, msg: Int8):
        self.ballPose_color = msg.data
        self.ballPose_last_rx = time.time() * 1000

    def GoToSilo(self, msg: Int8):
        self.silo_color = msg.data
        self.silo_last_rx = time.time() * 1000

    def GoToOrigin(self, msg: Int8):
        self.origin_color = msg.data
        self.origin_last_rx = time.time() * 1000

    def GoToMiddle(self, msg: Int8):
        self.middle_color = msg.data
        self.middle_last_rx = time.time() * 1000

    def RecoveryNode(self, msg: Int8):
        self.recovery_color = msg.data
        self.recovery_last_rx = time.time() * 1000
    
    def silo_number_callback(self, msg: UInt8):
        self.aligned_silo = msg

    def _reopen_serial_port(self):
        try:
            time.sleep(2)
            self.serial.close()
            self.serial = serial.Serial(
                serial_port_pico, serial_baudrate, timeout=1.0
            )
            logger.info("Serial port reopened successfully")

        except serial.SerialException as e:
            logger.error(f"Failed to reopen serial port: {e}")
        except OSError as e:
            logger.error(f"OSErorr::Failed to reopen serial port: {e}")
        except Exception as e:
            logger.error(f"Serial port unknown error: {e}")

    def calculate_checksum(self, data=[]):
        digest = int()
        for i in range(1, len(data)):
            digest += data[i]
        return int(digest)

    def calculate_crc(self, data=[]):
        hash_func = crc8()
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


if __name__ == "__main":
    main()
