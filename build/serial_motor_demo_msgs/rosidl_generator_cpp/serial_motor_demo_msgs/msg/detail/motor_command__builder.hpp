// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from serial_motor_demo_msgs:msg/MotorCommand.idl
// generated code does not contain a copyright notice

#ifndef SERIAL_MOTOR_DEMO_MSGS__MSG__DETAIL__MOTOR_COMMAND__BUILDER_HPP_
#define SERIAL_MOTOR_DEMO_MSGS__MSG__DETAIL__MOTOR_COMMAND__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "serial_motor_demo_msgs/msg/detail/motor_command__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace serial_motor_demo_msgs
{

namespace msg
{

namespace builder
{

class Init_MotorCommand_mot_2_req_rad_sec
{
public:
  explicit Init_MotorCommand_mot_2_req_rad_sec(::serial_motor_demo_msgs::msg::MotorCommand & msg)
  : msg_(msg)
  {}
  ::serial_motor_demo_msgs::msg::MotorCommand mot_2_req_rad_sec(::serial_motor_demo_msgs::msg::MotorCommand::_mot_2_req_rad_sec_type arg)
  {
    msg_.mot_2_req_rad_sec = std::move(arg);
    return std::move(msg_);
  }

private:
  ::serial_motor_demo_msgs::msg::MotorCommand msg_;
};

class Init_MotorCommand_mot_1_req_rad_sec
{
public:
  explicit Init_MotorCommand_mot_1_req_rad_sec(::serial_motor_demo_msgs::msg::MotorCommand & msg)
  : msg_(msg)
  {}
  Init_MotorCommand_mot_2_req_rad_sec mot_1_req_rad_sec(::serial_motor_demo_msgs::msg::MotorCommand::_mot_1_req_rad_sec_type arg)
  {
    msg_.mot_1_req_rad_sec = std::move(arg);
    return Init_MotorCommand_mot_2_req_rad_sec(msg_);
  }

private:
  ::serial_motor_demo_msgs::msg::MotorCommand msg_;
};

class Init_MotorCommand_is_pwm
{
public:
  Init_MotorCommand_is_pwm()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_MotorCommand_mot_1_req_rad_sec is_pwm(::serial_motor_demo_msgs::msg::MotorCommand::_is_pwm_type arg)
  {
    msg_.is_pwm = std::move(arg);
    return Init_MotorCommand_mot_1_req_rad_sec(msg_);
  }

private:
  ::serial_motor_demo_msgs::msg::MotorCommand msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::serial_motor_demo_msgs::msg::MotorCommand>()
{
  return serial_motor_demo_msgs::msg::builder::Init_MotorCommand_is_pwm();
}

}  // namespace serial_motor_demo_msgs

#endif  // SERIAL_MOTOR_DEMO_MSGS__MSG__DETAIL__MOTOR_COMMAND__BUILDER_HPP_
