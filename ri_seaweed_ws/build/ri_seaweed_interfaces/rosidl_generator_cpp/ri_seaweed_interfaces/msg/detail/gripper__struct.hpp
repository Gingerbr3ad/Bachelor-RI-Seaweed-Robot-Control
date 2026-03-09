// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from ri_seaweed_interfaces:msg/Gripper.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "ri_seaweed_interfaces/msg/gripper.hpp"


#ifndef RI_SEAWEED_INTERFACES__MSG__DETAIL__GRIPPER__STRUCT_HPP_
#define RI_SEAWEED_INTERFACES__MSG__DETAIL__GRIPPER__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__ri_seaweed_interfaces__msg__Gripper __attribute__((deprecated))
#else
# define DEPRECATED__ri_seaweed_interfaces__msg__Gripper __declspec(deprecated)
#endif

namespace ri_seaweed_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct Gripper_
{
  using Type = Gripper_<ContainerAllocator>;

  explicit Gripper_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->gripper_state = false;
      this->close_request = false;
    }
  }

  explicit Gripper_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->gripper_state = false;
      this->close_request = false;
    }
  }

  // field types and members
  using _gripper_state_type =
    bool;
  _gripper_state_type gripper_state;
  using _close_request_type =
    bool;
  _close_request_type close_request;

  // setters for named parameter idiom
  Type & set__gripper_state(
    const bool & _arg)
  {
    this->gripper_state = _arg;
    return *this;
  }
  Type & set__close_request(
    const bool & _arg)
  {
    this->close_request = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    ri_seaweed_interfaces::msg::Gripper_<ContainerAllocator> *;
  using ConstRawPtr =
    const ri_seaweed_interfaces::msg::Gripper_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<ri_seaweed_interfaces::msg::Gripper_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<ri_seaweed_interfaces::msg::Gripper_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      ri_seaweed_interfaces::msg::Gripper_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<ri_seaweed_interfaces::msg::Gripper_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      ri_seaweed_interfaces::msg::Gripper_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<ri_seaweed_interfaces::msg::Gripper_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<ri_seaweed_interfaces::msg::Gripper_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<ri_seaweed_interfaces::msg::Gripper_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__ri_seaweed_interfaces__msg__Gripper
    std::shared_ptr<ri_seaweed_interfaces::msg::Gripper_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__ri_seaweed_interfaces__msg__Gripper
    std::shared_ptr<ri_seaweed_interfaces::msg::Gripper_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const Gripper_ & other) const
  {
    if (this->gripper_state != other.gripper_state) {
      return false;
    }
    if (this->close_request != other.close_request) {
      return false;
    }
    return true;
  }
  bool operator!=(const Gripper_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct Gripper_

// alias to use template instance with default allocator
using Gripper =
  ri_seaweed_interfaces::msg::Gripper_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace ri_seaweed_interfaces

#endif  // RI_SEAWEED_INTERFACES__MSG__DETAIL__GRIPPER__STRUCT_HPP_
