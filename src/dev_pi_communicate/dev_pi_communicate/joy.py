#! /usr/bin/env python3

# from dev_pi_communicate.crc8 import crc8
import struct

from dev_pi_communicate.crc8 import crc8
START_BYTE_JOY= 0b10100101

class joy_buttons():
    def __init__(self):
        self.button_A = 0
        self.button_B = 0
        self.button_X = 0
        self.button_Y = 0
        self.button_LB = 0
        self.button_RB = 0
        self.button_back = 0
        self.button_start = 0
        self.button_power = 0
        self.button_stick_left = 0
        self.button_stick_right = 0
        self.button_up = 0
        self.button_down = 0

        self.axis_LT = 0.00
        self.axis_RT = 0.00

        self.axis_left_LR = 0.00
        self.axis_left_UD = 0.00
        self.axis_right_LR= 0.00
        self.axis_right_UD = 0.00
        self.axis_cross_LR = 0.00
        self.axis_cross_UD = 0.00


    def mapping(self):

        self.axis_left_LR = -(self.axis_left_LR * 126)
        self.axis_left_UD = (self.axis_left_UD * 126)
        self.axis_right_LR = -(self.axis_right_LR * 126)
        self.axis_right_UD = (self.axis_right_UD * 126)

        self.axis_LT = map(self.axis_LT, 1, -1, 0 , 255)
        self.axis_LT = map(self.axis_RT, 1, -1, 0 , 255)

def map(value, min_input, max_input, min_output, max_output):
    return (value*(max_output-min_output)/(max_input - min_input))


class packet_to_send():
    def __init__(self):
        self.payloadMask = bytes([
            0b00000001,
            0b00000010,
            0b00000100,
            0b00001000,
            0b00010000,
            0b00100000,
            0b01000000,
            0b10000000
        ])
        self.payload_antimask = bytes([
            0b11111110,
            0b11111101,
            0b11111011,
            0b11110111,
            0b11101111,
            0b11011111,
            0b10111111,
            0b01111111
        ])
        self.byte = [0]*10
    
    def create_packet(self,joy_bt=joy_buttons()):


        # assign start byte
        self.byte[0] = START_BYTE_JOY
        # crc_value = crc8()
        
        # byte 1
        if joy_bt.button_RB :
            self.byte[1] |= self.payloadMask[0]
        else:
            self.byte[1]  &= self.payload_antimask[0]

        if joy_bt.button_LB :
            self.byte[1] |= self.payloadMask[1]
        else:
            self.byte[1]  &= self.payload_antimask[1]

        if joy_bt.button_B :
            self.byte[1] |= self.payloadMask[4]
        else:
            self.byte[1]  &= self.payload_antimask[4]

        if joy_bt.button_A :
            self.byte[1] |= self.payloadMask[5]
        else:
            self.byte[1]  &= self.payload_antimask[5]
        if joy_bt.button_Y:
            self.byte[1] |= self.payloadMask[6]
        else:
            self.byte[1]  &= self.payload_antimask[6]
        if joy_bt.button_X:
            self.byte[1] |= self.payloadMask[7]
        else:
            self.byte[1]  &= self.payload_antimask[7]

        self.byte[2] = 0b00000000

        self.byte[3] = 0 #(int(joy_bt.axis_LT)  & 0xFF)
        self.byte[4] = 0 #(int(joy_bt.axis_RT) & 0xFF)

        self.byte[5] = int(joy_bt.axis_left_LR)  
        self.byte[6] = int(joy_bt.axis_left_UD)
        self.byte[7] = int(joy_bt.axis_right_LR)
        self.byte[8] = int(joy_bt.axis_right_UD)

        self.byte[9] = (self.calculate_crc(self.byte) & 0xFF)
        print(self.byte)
        

    def calculate_checksum(self , data = []*10):
        digest = int()
        for i in range(0,8):
            digest += data[i]
        return digest
    
    def calculate_crc(self, data=[]*10):
        hash_func=crc8()
        hash_func.update(data[1:-1])
        return hash_func.digest()[0]

