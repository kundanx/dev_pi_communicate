// generated from rosidl_typesupport_fastrtps_cpp/resource/idl__type_support.cpp.em
// with input from serial_motor_demo_msgs:msg/EncoderVals.idl
// generated code does not contain a copyright notice
#include "serial_motor_demo_msgs/msg/detail/encoder_vals__rosidl_typesupport_fastrtps_cpp.hpp"
#include "serial_motor_demo_msgs/msg/detail/encoder_vals__struct.hpp"

#include <limits>
#include <stdexcept>
#include <string>
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_fastrtps_cpp/identifier.hpp"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support_decl.hpp"
#include "rosidl_typesupport_fastrtps_cpp/wstring_conversion.hpp"
#include "fastcdr/Cdr.h"


// forward declaration of message dependencies and their conversion functions

namespace serial_motor_demo_msgs
{

namespace msg
{

namespace typesupport_fastrtps_cpp
{

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_serial_motor_demo_msgs
cdr_serialize(
  const serial_motor_demo_msgs::msg::EncoderVals & ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  // Member: mot_1_enc_val
  cdr << ros_message.mot_1_enc_val;
  // Member: mot_2_enc_val
  cdr << ros_message.mot_2_enc_val;
  return true;
}

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_serial_motor_demo_msgs
cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  serial_motor_demo_msgs::msg::EncoderVals & ros_message)
{
  // Member: mot_1_enc_val
  cdr >> ros_message.mot_1_enc_val;

  // Member: mot_2_enc_val
  cdr >> ros_message.mot_2_enc_val;

  return true;
}

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_serial_motor_demo_msgs
get_serialized_size(
  const serial_motor_demo_msgs::msg::EncoderVals & ros_message,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // Member: mot_1_enc_val
  {
    size_t item_size = sizeof(ros_message.mot_1_enc_val);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: mot_2_enc_val
  {
    size_t item_size = sizeof(ros_message.mot_2_enc_val);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  return current_alignment - initial_alignment;
}

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_serial_motor_demo_msgs
max_serialized_size_EncoderVals(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  full_bounded = true;
  is_plain = true;


  // Member: mot_1_enc_val
  {
    size_t array_size = 1;

    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  // Member: mot_2_enc_val
  {
    size_t array_size = 1;

    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  return current_alignment - initial_alignment;
}

static bool _EncoderVals__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  auto typed_message =
    static_cast<const serial_motor_demo_msgs::msg::EncoderVals *>(
    untyped_ros_message);
  return cdr_serialize(*typed_message, cdr);
}

static bool _EncoderVals__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  auto typed_message =
    static_cast<serial_motor_demo_msgs::msg::EncoderVals *>(
    untyped_ros_message);
  return cdr_deserialize(cdr, *typed_message);
}

static uint32_t _EncoderVals__get_serialized_size(
  const void * untyped_ros_message)
{
  auto typed_message =
    static_cast<const serial_motor_demo_msgs::msg::EncoderVals *>(
    untyped_ros_message);
  return static_cast<uint32_t>(get_serialized_size(*typed_message, 0));
}

static size_t _EncoderVals__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_EncoderVals(full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}

static message_type_support_callbacks_t _EncoderVals__callbacks = {
  "serial_motor_demo_msgs::msg",
  "EncoderVals",
  _EncoderVals__cdr_serialize,
  _EncoderVals__cdr_deserialize,
  _EncoderVals__get_serialized_size,
  _EncoderVals__max_serialized_size
};

static rosidl_message_type_support_t _EncoderVals__handle = {
  rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
  &_EncoderVals__callbacks,
  get_message_typesupport_handle_function,
};

}  // namespace typesupport_fastrtps_cpp

}  // namespace msg

}  // namespace serial_motor_demo_msgs

namespace rosidl_typesupport_fastrtps_cpp
{

template<>
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_EXPORT_serial_motor_demo_msgs
const rosidl_message_type_support_t *
get_message_type_support_handle<serial_motor_demo_msgs::msg::EncoderVals>()
{
  return &serial_motor_demo_msgs::msg::typesupport_fastrtps_cpp::_EncoderVals__handle;
}

}  // namespace rosidl_typesupport_fastrtps_cpp

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, serial_motor_demo_msgs, msg, EncoderVals)() {
  return &serial_motor_demo_msgs::msg::typesupport_fastrtps_cpp::_EncoderVals__handle;
}

#ifdef __cplusplus
}
#endif
