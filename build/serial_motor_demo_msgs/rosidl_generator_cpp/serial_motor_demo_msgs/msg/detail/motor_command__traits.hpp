// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from serial_motor_demo_msgs:msg/MotorCommand.idl
// generated code does not contain a copyright notice

#ifndef SERIAL_MOTOR_DEMO_MSGS__MSG__DETAIL__MOTOR_COMMAND__TRAITS_HPP_
#define SERIAL_MOTOR_DEMO_MSGS__MSG__DETAIL__MOTOR_COMMAND__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "serial_motor_demo_msgs/msg/detail/motor_command__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace serial_motor_demo_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const MotorCommand & msg,
  std::ostream & out)
{
  out << "{";
  // member: is_pwm
  {
    out << "is_pwm: ";
    rosidl_generator_traits::value_to_yaml(msg.is_pwm, out);
    out << ", ";
  }

  // member: mot_1_req_rad_sec
  {
    out << "mot_1_req_rad_sec: ";
    rosidl_generator_traits::value_to_yaml(msg.mot_1_req_rad_sec, out);
    out << ", ";
  }

  // member: mot_2_req_rad_sec
  {
    out << "mot_2_req_rad_sec: ";
    rosidl_generator_traits::value_to_yaml(msg.mot_2_req_rad_sec, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const MotorCommand & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: is_pwm
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "is_pwm: ";
    rosidl_generator_traits::value_to_yaml(msg.is_pwm, out);
    out << "\n";
  }

  // member: mot_1_req_rad_sec
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "mot_1_req_rad_sec: ";
    rosidl_generator_traits::value_to_yaml(msg.mot_1_req_rad_sec, out);
    out << "\n";
  }

  // member: mot_2_req_rad_sec
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "mot_2_req_rad_sec: ";
    rosidl_generator_traits::value_to_yaml(msg.mot_2_req_rad_sec, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const MotorCommand & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace serial_motor_demo_msgs

namespace rosidl_generator_traits
{

[[deprecated("use serial_motor_demo_msgs::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const serial_motor_demo_msgs::msg::MotorCommand & msg,
  std::ostream & out, size_t indentation = 0)
{
  serial_motor_demo_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use serial_motor_demo_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const serial_motor_demo_msgs::msg::MotorCommand & msg)
{
  return serial_motor_demo_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<serial_motor_demo_msgs::msg::MotorCommand>()
{
  return "serial_motor_demo_msgs::msg::MotorCommand";
}

template<>
inline const char * name<serial_motor_demo_msgs::msg::MotorCommand>()
{
  return "serial_motor_demo_msgs/msg/MotorCommand";
}

template<>
struct has_fixed_size<serial_motor_demo_msgs::msg::MotorCommand>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<serial_motor_demo_msgs::msg::MotorCommand>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<serial_motor_demo_msgs::msg::MotorCommand>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // SERIAL_MOTOR_DEMO_MSGS__MSG__DETAIL__MOTOR_COMMAND__TRAITS_HPP_
