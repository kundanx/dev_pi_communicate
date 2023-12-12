// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from serial_motor_demo_msgs:msg/EncoderVals.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "serial_motor_demo_msgs/msg/detail/encoder_vals__rosidl_typesupport_introspection_c.h"
#include "serial_motor_demo_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "serial_motor_demo_msgs/msg/detail/encoder_vals__functions.h"
#include "serial_motor_demo_msgs/msg/detail/encoder_vals__struct.h"


#ifdef __cplusplus
extern "C"
{
#endif

void serial_motor_demo_msgs__msg__EncoderVals__rosidl_typesupport_introspection_c__EncoderVals_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  serial_motor_demo_msgs__msg__EncoderVals__init(message_memory);
}

void serial_motor_demo_msgs__msg__EncoderVals__rosidl_typesupport_introspection_c__EncoderVals_fini_function(void * message_memory)
{
  serial_motor_demo_msgs__msg__EncoderVals__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember serial_motor_demo_msgs__msg__EncoderVals__rosidl_typesupport_introspection_c__EncoderVals_message_member_array[2] = {
  {
    "mot_1_enc_val",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT32,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(serial_motor_demo_msgs__msg__EncoderVals, mot_1_enc_val),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "mot_2_enc_val",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT32,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(serial_motor_demo_msgs__msg__EncoderVals, mot_2_enc_val),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers serial_motor_demo_msgs__msg__EncoderVals__rosidl_typesupport_introspection_c__EncoderVals_message_members = {
  "serial_motor_demo_msgs__msg",  // message namespace
  "EncoderVals",  // message name
  2,  // number of fields
  sizeof(serial_motor_demo_msgs__msg__EncoderVals),
  serial_motor_demo_msgs__msg__EncoderVals__rosidl_typesupport_introspection_c__EncoderVals_message_member_array,  // message members
  serial_motor_demo_msgs__msg__EncoderVals__rosidl_typesupport_introspection_c__EncoderVals_init_function,  // function to initialize message memory (memory has to be allocated)
  serial_motor_demo_msgs__msg__EncoderVals__rosidl_typesupport_introspection_c__EncoderVals_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t serial_motor_demo_msgs__msg__EncoderVals__rosidl_typesupport_introspection_c__EncoderVals_message_type_support_handle = {
  0,
  &serial_motor_demo_msgs__msg__EncoderVals__rosidl_typesupport_introspection_c__EncoderVals_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_serial_motor_demo_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, serial_motor_demo_msgs, msg, EncoderVals)() {
  if (!serial_motor_demo_msgs__msg__EncoderVals__rosidl_typesupport_introspection_c__EncoderVals_message_type_support_handle.typesupport_identifier) {
    serial_motor_demo_msgs__msg__EncoderVals__rosidl_typesupport_introspection_c__EncoderVals_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &serial_motor_demo_msgs__msg__EncoderVals__rosidl_typesupport_introspection_c__EncoderVals_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
