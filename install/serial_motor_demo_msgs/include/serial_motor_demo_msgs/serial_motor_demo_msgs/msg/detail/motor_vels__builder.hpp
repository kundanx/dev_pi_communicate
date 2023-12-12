// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from serial_motor_demo_msgs:msg/MotorVels.idl
// generated code does not contain a copyright notice

#ifndef SERIAL_MOTOR_DEMO_MSGS__MSG__DETAIL__MOTOR_VELS__BUILDER_HPP_
#define SERIAL_MOTOR_DEMO_MSGS__MSG__DETAIL__MOTOR_VELS__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "serial_motor_demo_msgs/msg/detail/motor_vels__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace serial_motor_demo_msgs
{

namespace msg
{

namespace builder
{

class Init_MotorVels_mot_2_rad_sec
{
public:
  explicit Init_MotorVels_mot_2_rad_sec(::serial_motor_demo_msgs::msg::MotorVels & msg)
  : msg_(msg)
  {}
  ::serial_motor_demo_msgs::msg::MotorVels mot_2_rad_sec(::serial_motor_demo_msgs::msg::MotorVels::_mot_2_rad_sec_type arg)
  {
    msg_.mot_2_rad_sec = std::move(arg);
    return std::move(msg_);
  }

private:
  ::serial_motor_demo_msgs::msg::MotorVels msg_;
};

class Init_MotorVels_mot_1_rad_sec
{
public:
  Init_MotorVels_mot_1_rad_sec()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_MotorVels_mot_2_rad_sec mot_1_rad_sec(::serial_motor_demo_msgs::msg::MotorVels::_mot_1_rad_sec_type arg)
  {
    msg_.mot_1_rad_sec = std::move(arg);
    return Init_MotorVels_mot_2_rad_sec(msg_);
  }

private:
  ::serial_motor_demo_msgs::msg::MotorVels msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::serial_motor_demo_msgs::msg::MotorVels>()
{
  return serial_motor_demo_msgs::msg::builder::Init_MotorVels_mot_1_rad_sec();
}

}  // namespace serial_motor_demo_msgs

#endif  // SERIAL_MOTOR_DEMO_MSGS__MSG__DETAIL__MOTOR_VELS__BUILDER_HPP_
