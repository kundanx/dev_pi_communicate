// generated from rosidl_typesupport_introspection_cpp/resource/idl__type_support.cpp.em
// with input from serial_motor_demo_msgs:msg/EncoderVals.idl
// generated code does not contain a copyright notice

#include "array"
#include "cstddef"
#include "string"
#include "vector"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_interface/macros.h"
#include "serial_motor_demo_msgs/msg/detail/encoder_vals__struct.hpp"
#include "rosidl_typesupport_introspection_cpp/field_types.hpp"
#include "rosidl_typesupport_introspection_cpp/identifier.hpp"
#include "rosidl_typesupport_introspection_cpp/message_introspection.hpp"
#include "rosidl_typesupport_introspection_cpp/message_type_support_decl.hpp"
#include "rosidl_typesupport_introspection_cpp/visibility_control.h"

namespace serial_motor_demo_msgs
{

namespace msg
{

namespace rosidl_typesupport_introspection_cpp
{

void EncoderVals_init_function(
  void * message_memory, rosidl_runtime_cpp::MessageInitialization _init)
{
  new (message_memory) serial_motor_demo_msgs::msg::EncoderVals(_init);
}

void EncoderVals_fini_function(void * message_memory)
{
  auto typed_message = static_cast<serial_motor_demo_msgs::msg::EncoderVals *>(message_memory);
  typed_message->~EncoderVals();
}

static const ::rosidl_typesupport_introspection_cpp::MessageMember EncoderVals_message_member_array[2] = {
  {
    "mot_1_enc_val",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_INT32,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(serial_motor_demo_msgs::msg::EncoderVals, mot_1_enc_val),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "mot_2_enc_val",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_INT32,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(serial_motor_demo_msgs::msg::EncoderVals, mot_2_enc_val),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  }
};

static const ::rosidl_typesupport_introspection_cpp::MessageMembers EncoderVals_message_members = {
  "serial_motor_demo_msgs::msg",  // message namespace
  "EncoderVals",  // message name
  2,  // number of fields
  sizeof(serial_motor_demo_msgs::msg::EncoderVals),
  EncoderVals_message_member_array,  // message members
  EncoderVals_init_function,  // function to initialize message memory (memory has to be allocated)
  EncoderVals_fini_function  // function to terminate message instance (will not free memory)
};

static const rosidl_message_type_support_t EncoderVals_message_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &EncoderVals_message_members,
  get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_introspection_cpp

}  // namespace msg

}  // namespace serial_motor_demo_msgs


namespace rosidl_typesupport_introspection_cpp
{

template<>
ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<serial_motor_demo_msgs::msg::EncoderVals>()
{
  return &::serial_motor_demo_msgs::msg::rosidl_typesupport_introspection_cpp::EncoderVals_message_type_support_handle;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, serial_motor_demo_msgs, msg, EncoderVals)() {
  return &::serial_motor_demo_msgs::msg::rosidl_typesupport_introspection_cpp::EncoderVals_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif
