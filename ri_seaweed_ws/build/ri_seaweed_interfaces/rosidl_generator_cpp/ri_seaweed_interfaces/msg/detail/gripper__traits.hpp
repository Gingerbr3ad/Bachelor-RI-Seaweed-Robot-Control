// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from ri_seaweed_interfaces:msg/Gripper.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "ri_seaweed_interfaces/msg/gripper.hpp"


#ifndef RI_SEAWEED_INTERFACES__MSG__DETAIL__GRIPPER__TRAITS_HPP_
#define RI_SEAWEED_INTERFACES__MSG__DETAIL__GRIPPER__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "ri_seaweed_interfaces/msg/detail/gripper__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace ri_seaweed_interfaces
{

namespace msg
{

inline void to_flow_style_yaml(
  const Gripper & msg,
  std::ostream & out)
{
  out << "{";
  // member: gripper_state
  {
    out << "gripper_state: ";
    rosidl_generator_traits::value_to_yaml(msg.gripper_state, out);
    out << ", ";
  }

  // member: close_request
  {
    out << "close_request: ";
    rosidl_generator_traits::value_to_yaml(msg.close_request, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const Gripper & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: gripper_state
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "gripper_state: ";
    rosidl_generator_traits::value_to_yaml(msg.gripper_state, out);
    out << "\n";
  }

  // member: close_request
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "close_request: ";
    rosidl_generator_traits::value_to_yaml(msg.close_request, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Gripper & msg, bool use_flow_style = false)
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

}  // namespace ri_seaweed_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use ri_seaweed_interfaces::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const ri_seaweed_interfaces::msg::Gripper & msg,
  std::ostream & out, size_t indentation = 0)
{
  ri_seaweed_interfaces::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use ri_seaweed_interfaces::msg::to_yaml() instead")]]
inline std::string to_yaml(const ri_seaweed_interfaces::msg::Gripper & msg)
{
  return ri_seaweed_interfaces::msg::to_yaml(msg);
}

template<>
inline const char * data_type<ri_seaweed_interfaces::msg::Gripper>()
{
  return "ri_seaweed_interfaces::msg::Gripper";
}

template<>
inline const char * name<ri_seaweed_interfaces::msg::Gripper>()
{
  return "ri_seaweed_interfaces/msg/Gripper";
}

template<>
struct has_fixed_size<ri_seaweed_interfaces::msg::Gripper>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<ri_seaweed_interfaces::msg::Gripper>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<ri_seaweed_interfaces::msg::Gripper>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // RI_SEAWEED_INTERFACES__MSG__DETAIL__GRIPPER__TRAITS_HPP_
