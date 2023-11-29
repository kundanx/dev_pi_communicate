// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from serial_motor_demo_msgs:msg/EncoderVals.idl
// generated code does not contain a copyright notice

#ifndef SERIAL_MOTOR_DEMO_MSGS__MSG__DETAIL__ENCODER_VALS__STRUCT_HPP_
#define SERIAL_MOTOR_DEMO_MSGS__MSG__DETAIL__ENCODER_VALS__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__serial_motor_demo_msgs__msg__EncoderVals __attribute__((deprecated))
#else
# define DEPRECATED__serial_motor_demo_msgs__msg__EncoderVals __declspec(deprecated)
#endif

namespace serial_motor_demo_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct EncoderVals_
{
  using Type = EncoderVals_<ContainerAllocator>;

  explicit EncoderVals_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->mot_1_enc_val = 0l;
      this->mot_2_enc_val = 0l;
    }
  }

  explicit EncoderVals_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->mot_1_enc_val = 0l;
      this->mot_2_enc_val = 0l;
    }
  }

  // field types and members
  using _mot_1_enc_val_type =
    int32_t;
  _mot_1_enc_val_type mot_1_enc_val;
  using _mot_2_enc_val_type =
    int32_t;
  _mot_2_enc_val_type mot_2_enc_val;

  // setters for named parameter idiom
  Type & set__mot_1_enc_val(
    const int32_t & _arg)
  {
    this->mot_1_enc_val = _arg;
    return *this;
  }
  Type & set__mot_2_enc_val(
    const int32_t & _arg)
  {
    this->mot_2_enc_val = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    serial_motor_demo_msgs::msg::EncoderVals_<ContainerAllocator> *;
  using ConstRawPtr =
    const serial_motor_demo_msgs::msg::EncoderVals_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<serial_motor_demo_msgs::msg::EncoderVals_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<serial_motor_demo_msgs::msg::EncoderVals_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      serial_motor_demo_msgs::msg::EncoderVals_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<serial_motor_demo_msgs::msg::EncoderVals_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      serial_motor_demo_msgs::msg::EncoderVals_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<serial_motor_demo_msgs::msg::EncoderVals_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<serial_motor_demo_msgs::msg::EncoderVals_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<serial_motor_demo_msgs::msg::EncoderVals_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__serial_motor_demo_msgs__msg__EncoderVals
    std::shared_ptr<serial_motor_demo_msgs::msg::EncoderVals_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__serial_motor_demo_msgs__msg__EncoderVals
    std::shared_ptr<serial_motor_demo_msgs::msg::EncoderVals_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const EncoderVals_ & other) const
  {
    if (this->mot_1_enc_val != other.mot_1_enc_val) {
      return false;
    }
    if (this->mot_2_enc_val != other.mot_2_enc_val) {
      return false;
    }
    return true;
  }
  bool operator!=(const EncoderVals_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct EncoderVals_

// alias to use template instance with default allocator
using EncoderVals =
  serial_motor_demo_msgs::msg::EncoderVals_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace serial_motor_demo_msgs

#endif  // SERIAL_MOTOR_DEMO_MSGS__MSG__DETAIL__ENCODER_VALS__STRUCT_HPP_
