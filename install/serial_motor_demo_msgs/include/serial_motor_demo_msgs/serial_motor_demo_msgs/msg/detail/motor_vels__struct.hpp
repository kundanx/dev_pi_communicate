// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from serial_motor_demo_msgs:msg/MotorVels.idl
// generated code does not contain a copyright notice

#ifndef SERIAL_MOTOR_DEMO_MSGS__MSG__DETAIL__MOTOR_VELS__STRUCT_HPP_
#define SERIAL_MOTOR_DEMO_MSGS__MSG__DETAIL__MOTOR_VELS__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__serial_motor_demo_msgs__msg__MotorVels __attribute__((deprecated))
#else
# define DEPRECATED__serial_motor_demo_msgs__msg__MotorVels __declspec(deprecated)
#endif

namespace serial_motor_demo_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct MotorVels_
{
  using Type = MotorVels_<ContainerAllocator>;

  explicit MotorVels_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->mot_1_rad_sec = 0.0f;
      this->mot_2_rad_sec = 0.0f;
    }
  }

  explicit MotorVels_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->mot_1_rad_sec = 0.0f;
      this->mot_2_rad_sec = 0.0f;
    }
  }

  // field types and members
  using _mot_1_rad_sec_type =
    float;
  _mot_1_rad_sec_type mot_1_rad_sec;
  using _mot_2_rad_sec_type =
    float;
  _mot_2_rad_sec_type mot_2_rad_sec;

  // setters for named parameter idiom
  Type & set__mot_1_rad_sec(
    const float & _arg)
  {
    this->mot_1_rad_sec = _arg;
    return *this;
  }
  Type & set__mot_2_rad_sec(
    const float & _arg)
  {
    this->mot_2_rad_sec = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    serial_motor_demo_msgs::msg::MotorVels_<ContainerAllocator> *;
  using ConstRawPtr =
    const serial_motor_demo_msgs::msg::MotorVels_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<serial_motor_demo_msgs::msg::MotorVels_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<serial_motor_demo_msgs::msg::MotorVels_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      serial_motor_demo_msgs::msg::MotorVels_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<serial_motor_demo_msgs::msg::MotorVels_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      serial_motor_demo_msgs::msg::MotorVels_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<serial_motor_demo_msgs::msg::MotorVels_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<serial_motor_demo_msgs::msg::MotorVels_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<serial_motor_demo_msgs::msg::MotorVels_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__serial_motor_demo_msgs__msg__MotorVels
    std::shared_ptr<serial_motor_demo_msgs::msg::MotorVels_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__serial_motor_demo_msgs__msg__MotorVels
    std::shared_ptr<serial_motor_demo_msgs::msg::MotorVels_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const MotorVels_ & other) const
  {
    if (this->mot_1_rad_sec != other.mot_1_rad_sec) {
      return false;
    }
    if (this->mot_2_rad_sec != other.mot_2_rad_sec) {
      return false;
    }
    return true;
  }
  bool operator!=(const MotorVels_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct MotorVels_

// alias to use template instance with default allocator
using MotorVels =
  serial_motor_demo_msgs::msg::MotorVels_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace serial_motor_demo_msgs

#endif  // SERIAL_MOTOR_DEMO_MSGS__MSG__DETAIL__MOTOR_VELS__STRUCT_HPP_
