// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from serial_motor_demo_msgs:msg/EncoderVals.idl
// generated code does not contain a copyright notice

#ifndef SERIAL_MOTOR_DEMO_MSGS__MSG__DETAIL__ENCODER_VALS__STRUCT_H_
#define SERIAL_MOTOR_DEMO_MSGS__MSG__DETAIL__ENCODER_VALS__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in msg/EncoderVals in the package serial_motor_demo_msgs.
typedef struct serial_motor_demo_msgs__msg__EncoderVals
{
  int32_t mot_1_enc_val;
  int32_t mot_2_enc_val;
} serial_motor_demo_msgs__msg__EncoderVals;

// Struct for a sequence of serial_motor_demo_msgs__msg__EncoderVals.
typedef struct serial_motor_demo_msgs__msg__EncoderVals__Sequence
{
  serial_motor_demo_msgs__msg__EncoderVals * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} serial_motor_demo_msgs__msg__EncoderVals__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // SERIAL_MOTOR_DEMO_MSGS__MSG__DETAIL__ENCODER_VALS__STRUCT_H_
