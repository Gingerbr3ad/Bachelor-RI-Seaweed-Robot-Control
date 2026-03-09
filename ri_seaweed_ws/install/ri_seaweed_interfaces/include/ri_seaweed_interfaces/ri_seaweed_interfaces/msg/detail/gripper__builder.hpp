// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from ri_seaweed_interfaces:msg/Gripper.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "ri_seaweed_interfaces/msg/gripper.hpp"


#ifndef RI_SEAWEED_INTERFACES__MSG__DETAIL__GRIPPER__BUILDER_HPP_
#define RI_SEAWEED_INTERFACES__MSG__DETAIL__GRIPPER__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "ri_seaweed_interfaces/msg/detail/gripper__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace ri_seaweed_interfaces
{

namespace msg
{

namespace builder
{

class Init_Gripper_close_request
{
public:
  explicit Init_Gripper_close_request(::ri_seaweed_interfaces::msg::Gripper & msg)
  : msg_(msg)
  {}
  ::ri_seaweed_interfaces::msg::Gripper close_request(::ri_seaweed_interfaces::msg::Gripper::_close_request_type arg)
  {
    msg_.close_request = std::move(arg);
    return std::move(msg_);
  }

private:
  ::ri_seaweed_interfaces::msg::Gripper msg_;
};

class Init_Gripper_gripper_state
{
public:
  Init_Gripper_gripper_state()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Gripper_close_request gripper_state(::ri_seaweed_interfaces::msg::Gripper::_gripper_state_type arg)
  {
    msg_.gripper_state = std::move(arg);
    return Init_Gripper_close_request(msg_);
  }

private:
  ::ri_seaweed_interfaces::msg::Gripper msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::ri_seaweed_interfaces::msg::Gripper>()
{
  return ri_seaweed_interfaces::msg::builder::Init_Gripper_gripper_state();
}

}  // namespace ri_seaweed_interfaces

#endif  // RI_SEAWEED_INTERFACES__MSG__DETAIL__GRIPPER__BUILDER_HPP_
