#! /usr/bin/env python3
import rclpy
import serial
import struct

from rclpy.node import Node 
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Point
from nav_msgs.msg import Odometry

from dev_pi_communicate.joy import packet_to_send
from dev_pi_communicate.camera import packet_to_send_camera
from dev_pi_communicate.crc8 import crc8

START_BYTE = bytes.fromhex('A5')

DATA_LENGTH = 10

class vel_data:
    def __init__(self):
        self.linear_x=0.00
        self.linear_y=0.00
        self.linear_z=0.00

        self.angular_x=0.00
        self.angular_y=0.00
        self.angular_z=0.00

    
class serial_comms:
    def __init__(self, serial_port, serial_baudrate):
        self.serial = serial.Serial(serial_port, serial_baudrate)

        
    def send_vel(self, vel_x, vel_y, vel_z,ang_x,ang_y,ang_z):
        
        #data_to_send= struct.pack("f f f", vel_x, vel_y, vel_z) #  + struct.pack("f", vel_y)+struct.pack("f",vel_z)
        data_to_send = [
            bytes(struct.pack("f", vel_x)),
            bytes(struct.pack("f", vel_y)),
            bytes(struct.pack("f", vel_z)),
            bytes(struct.pack("f", ang_x)),
            bytes(struct.pack("f", ang_y)),
            bytes(struct.pack("f", ang_z))
            ]
        data_to_send = b''.join(data_to_send)
        data_to_send = START_BYTE + data_to_send
        print(data_to_send)
        print(f"{len(data_to_send)=}")
        self.serial.write(data_to_send)
        # return data_to_send
    
    def send_camera_data(self, byte=packet_to_send_camera()):
        camera_data_to_send = [
            bytes(struct.pack("B", byte.data_to_send_camera[0])),
            bytes(struct.pack('f', byte.data_to_send_camera[1])),
            bytes(struct.pack('f', byte.data_to_send_camera[2])),
            bytes(struct.pack('f', byte.data_to_send_camera[3])),
            bytes(struct.pack('B', byte.data_to_send_camera[4]))
        ]
        camera_data_to_send = b''.join(camera_data_to_send)
        print(camera_data_to_send)
        self.serial.write(camera_data_to_send)
    
    def send_joy_data(self, data= packet_to_send()):
        joy_data_to_send =[
            bytes(struct.pack("B",data.byte[0])),
            bytes(struct.pack("B",data.byte[1])),
            bytes(struct.pack("B",data.byte[2])),
            bytes(struct.pack("B",data.byte[3])),
            bytes(struct.pack("B",data.byte[4])),
            bytes(struct.pack("b",data.byte[5])),
            bytes(struct.pack("b",data.byte[6])),
            bytes(struct.pack("b",data.byte[7])),
            bytes(struct.pack("b",data.byte[8])),
            bytes(struct.pack("B",data.byte[9]))
        ]
        joy_data_to_send= b''.join(joy_data_to_send)
        # print(joy_data_to_send)
        self.serial.write(joy_data_to_send)
    
    def read(self):
        while True:
            start_byte_found = False
            while not start_byte_found:
                byte = self.serial.read(1)
                if byte == START_BYTE:
                    data_str = self.serial.read(9)
                    start_byte_found=True
                    print(data_str)
          
            hash = self.calculate_crc(data_str)
            if hash == data_str[-1]:
                return data_str
            
            # print(data_str)
            # for i in range(0,7):
            #     checksum = checksum ^ data_str[i]
            #     print(checksum)
            # if checksum == data_str[7]:
            #     return  data_str

            print("data not matched")
    
    def calculate_crc(self, data=[]*9):
        hash_func=crc8()
        hash_func.update(data[0:-1])
        return hash_func.digest()[0]

    
    def __del__(self):
        self.serial.close()
        

class Serial_comms_node(Node):
    
    def __init__(self):
        # initiallize a node with namne: serial_comm_node
        super().__init__("serial_comm_node")
        self.declare_parameter('usb_serial_port')
        self.data= vel_data()
      

        self.recieved_data_pub = self.create_publisher(Point,'/recieved_data_topic', 10)
        self.create_timer(0.5, self.serial_read_callback)
        self.get_logger().info("Recieving data")
       

        # object of class Serial for serial transmission
        self.serial_baudrate = 115200
        # self.serial_port='/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A50285BI-if00-port0'
        global serial_comms_interface
        self.serial_comms_interface = serial_comms( 
            '/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A50285BI-if00-port0',
            self.serial_baudrate
        )
        

        # subsrcriber to listen data from terminal
        self.cmd_vel_sub = self.create_subscription(
            Twist,
            "cmd_vel",
            self.callback, 
            10
        )
        # self.timer = self.create_timer(0.1, self.serial_read_callback)
    
    def serial_read_callback(self):
            data = self.serial_comms_interface.read()
            data= struct.unpack('BBBBBBBBB', data)

            odometry_data = Point()
            odometry_data.x=float(data[0])
            odometry_data.y=float(data[1])
            odometry_data.z=float(data[2])

            self.recieved_data_pub.publish(odometry_data)
            print(data)
            
    def callback(self,msg:Twist):
        
        self.data.linear_x= msg.linear.x
        self.data.linear_y= msg.linear.y
        self.data.linear_z= msg.linear.z

        self.data.angular_x=msg.angular.x
        self.data.angular_y=msg.angular.y
        self.data.angular_z=msg.angular.z

        self.serial_comms_interface.send_vel(self.data.linear_x, self.data.linear_y, self.data.linear_z,
                                             self.data.angular_x, self.data.angular_y, self.data.angular_z)    

def main(args=None):
    rclpy.init()
    serial_node = Serial_comms_node()
    rclpy.spin(serial_node)
    rclpy.shutdown()
   
if __name__ =='__main':
    main()
