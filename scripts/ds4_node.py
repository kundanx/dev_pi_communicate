#! /usr/bin/env python3

# This node recieves data from ds4_uart_node and computes the velocity command and publishes to serial_tx_node

import rclpy
from sensor_msgs.msg import Joy
from std_msgs.msg import Float64MultiArray

MAX_VELOCITY = 0.15
MAX_OMEGA = 0.3

isEmergencyBrake = False

def joy_callback(msg):
    global isEmergencyBrake

    # print(msg.axes)

    if (msg.buttons[4] == 1):
        speedFactor = 0.2
    else:
        speedFactor = 1.0

    # Map left joystick to velocity_x and velocity_y
    vx = map_value(msg.axes[0], -1.0, 1.0, -MAX_VELOCITY, MAX_VELOCITY) * speedFactor   # X-axis of left joystick
    vy = map_value(msg.axes[1], -1.0,  1.0, -MAX_VELOCITY, MAX_VELOCITY) * speedFactor  # Y-axis of left joystick
    
    # Map L2 and R2 to omega
    w = map_value(msg.axes[4] - msg.axes[5], -1.0, 1.0, -MAX_OMEGA, MAX_OMEGA) * speedFactor  # L2 - R2

    # if ((msg.axes[6] != 0) | (msg.axes[7] != 0)):
    #     vy = msg.axes[7] * MAX_VELOCITY * speedFactor
    #     vx = -msg.axes[6] * MAX_VELOCITY * speedFactor

    if (msg.buttons[13]):
        isEmergencyBrake = True

    if (msg.buttons[8] and msg.buttons[9] and msg.buttons[13]):
        isEmergencyBrake = False

    if (isEmergencyBrake):
        vx = vy = w = 0.0
    
    # print(msg.buttons)
    set_speed(vx, vy, w)


def set_speed(vx, vy, w):
    twist_array = Float64MultiArray()
    twist_array.data = [vx, vy, w]
    # print(twist_array.data[0], twist_array.data[1], twist_array.data[2])
    pub.publish(twist_array)


def map_value(value, min_value, max_value, new_min, new_max):
    mapped_value = ((value - min_value) * (new_max - new_min)) / (max_value - min_value) + new_min
    return mapped_value


def main():
    rclpy.init()
    node = rclpy.create_node('ds4_controller')

    global pub
    pub = node.create_publisher(Float64MultiArray, '/cmd_robot_vel', 10)
    sub = node.create_subscription(Joy, '/joy', joy_callback, 10)

    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()


