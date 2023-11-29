// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from serial_motor_demo_msgs:msg/MotorVels.idl
// generated code does not contain a copyright notice

#ifndef SERIAL_MOTOR_DEMO_MSGS__MSG__DETAIL__MOTOR_VELS__STRUCT_H_
#define SERIAL_MOTOR_DEMO_MSGS__MSG__DETAIL__MOTOR_VELS__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in msg/MotorVels in the package serial_motor_demo_msgs.
typedef struct serial_motor_demo_msgs__msg__MotorVels
{
  float mot_1_rad_sec;
  float mot_2_rad_sec;
} serial_motor_demo_msgs__msg__MotorVels;

// Struct for a sequence of serial_motor_demo_msgs__msg__MotorVels.
typedef struct serial_motor_demo_msgs__msg__MotorVels__Sequence
{
  serial_motor_demo_msgs__msg__MotorVels * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} serial_motor_demo_msgs__msg__MotorVels__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // SERIAL_MOTOR_DEMO_MSGS__MSG__DETAIL__MOTOR_VELS__STRUCT_H_
