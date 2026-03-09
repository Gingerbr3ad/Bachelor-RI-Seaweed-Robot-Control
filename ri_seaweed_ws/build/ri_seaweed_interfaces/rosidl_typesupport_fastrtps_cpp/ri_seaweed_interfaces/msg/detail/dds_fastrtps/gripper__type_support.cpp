// generated from rosidl_typesupport_fastrtps_cpp/resource/idl__type_support.cpp.em
// with input from ri_seaweed_interfaces:msg/Gripper.idl
// generated code does not contain a copyright notice
#include "ri_seaweed_interfaces/msg/detail/gripper__rosidl_typesupport_fastrtps_cpp.hpp"
#include "ri_seaweed_interfaces/msg/detail/gripper__functions.h"
#include "ri_seaweed_interfaces/msg/detail/gripper__struct.hpp"

#include <cstddef>
#include <limits>
#include <stdexcept>
#include <string>
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_fastrtps_cpp/identifier.hpp"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support_decl.hpp"
#include "rosidl_typesupport_fastrtps_cpp/serialization_helpers.hpp"
#include "rosidl_typesupport_fastrtps_cpp/wstring_conversion.hpp"
#include "fastcdr/Cdr.h"


// forward declaration of message dependencies and their conversion functions

namespace ri_seaweed_interfaces
{

namespace msg
{

namespace typesupport_fastrtps_cpp
{


bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_ri_seaweed_interfaces
cdr_serialize(
  const ri_seaweed_interfaces::msg::Gripper & ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  // Member: gripper_state
  cdr << (ros_message.gripper_state ? true : false);

  // Member: close_request
  cdr << (ros_message.close_request ? true : false);

  return true;
}

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_ri_seaweed_interfaces
cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  ri_seaweed_interfaces::msg::Gripper & ros_message)
{
  // Member: gripper_state
  {
    uint8_t tmp;
    cdr >> tmp;
    ros_message.gripper_state = tmp ? true : false;
  }

  // Member: close_request
  {
    uint8_t tmp;
    cdr >> tmp;
    ros_message.close_request = tmp ? true : false;
  }

  return true;
}  // NOLINT(readability/fn_size)


size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_ri_seaweed_interfaces
get_serialized_size(
  const ri_seaweed_interfaces::msg::Gripper & ros_message,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // Member: gripper_state
  {
    size_t item_size = sizeof(ros_message.gripper_state);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Member: close_request
  {
    size_t item_size = sizeof(ros_message.close_request);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  return current_alignment - initial_alignment;
}


size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_ri_seaweed_interfaces
max_serialized_size_Gripper(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  size_t last_member_size = 0;
  (void)last_member_size;
  (void)padding;
  (void)wchar_size;

  full_bounded = true;
  is_plain = true;

  // Member: gripper_state
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }
  // Member: close_request
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }

  size_t ret_val = current_alignment - initial_alignment;
  if (is_plain) {
    // All members are plain, and type is not empty.
    // We still need to check that the in-memory alignment
    // is the same as the CDR mandated alignment.
    using DataType = ri_seaweed_interfaces::msg::Gripper;
    is_plain =
      (
      offsetof(DataType, close_request) +
      last_member_size
      ) == ret_val;
  }

  return ret_val;
}

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_ri_seaweed_interfaces
cdr_serialize_key(
  const ri_seaweed_interfaces::msg::Gripper & ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  // Member: gripper_state
  cdr << (ros_message.gripper_state ? true : false);

  // Member: close_request
  cdr << (ros_message.close_request ? true : false);

  return true;
}

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_ri_seaweed_interfaces
get_serialized_size_key(
  const ri_seaweed_interfaces::msg::Gripper & ros_message,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // Member: gripper_state
  {
    size_t item_size = sizeof(ros_message.gripper_state);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  // Member: close_request
  {
    size_t item_size = sizeof(ros_message.close_request);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  return current_alignment - initial_alignment;
}

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_ri_seaweed_interfaces
max_serialized_size_key_Gripper(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  size_t last_member_size = 0;
  (void)last_member_size;
  (void)padding;
  (void)wchar_size;

  full_bounded = true;
  is_plain = true;

  // Member: gripper_state
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }

  // Member: close_request
  {
    size_t array_size = 1;
    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }

  size_t ret_val = current_alignment - initial_alignment;
  if (is_plain) {
    // All members are plain, and type is not empty.
    // We still need to check that the in-memory alignment
    // is the same as the CDR mandated alignment.
    using DataType = ri_seaweed_interfaces::msg::Gripper;
    is_plain =
      (
      offsetof(DataType, close_request) +
      last_member_size
      ) == ret_val;
  }

  return ret_val;
}


static bool _Gripper__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  auto typed_message =
    static_cast<const ri_seaweed_interfaces::msg::Gripper *>(
    untyped_ros_message);
  return cdr_serialize(*typed_message, cdr);
}

static bool _Gripper__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  auto typed_message =
    static_cast<ri_seaweed_interfaces::msg::Gripper *>(
    untyped_ros_message);
  return cdr_deserialize(cdr, *typed_message);
}

static uint32_t _Gripper__get_serialized_size(
  const void * untyped_ros_message)
{
  auto typed_message =
    static_cast<const ri_seaweed_interfaces::msg::Gripper *>(
    untyped_ros_message);
  return static_cast<uint32_t>(get_serialized_size(*typed_message, 0));
}

static size_t _Gripper__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_Gripper(full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}

static message_type_support_callbacks_t _Gripper__callbacks = {
  "ri_seaweed_interfaces::msg",
  "Gripper",
  _Gripper__cdr_serialize,
  _Gripper__cdr_deserialize,
  _Gripper__get_serialized_size,
  _Gripper__max_serialized_size,
  nullptr
};

static rosidl_message_type_support_t _Gripper__handle = {
  rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
  &_Gripper__callbacks,
  get_message_typesupport_handle_function,
  &ri_seaweed_interfaces__msg__Gripper__get_type_hash,
  &ri_seaweed_interfaces__msg__Gripper__get_type_description,
  &ri_seaweed_interfaces__msg__Gripper__get_type_description_sources,
};

}  // namespace typesupport_fastrtps_cpp

}  // namespace msg

}  // namespace ri_seaweed_interfaces

namespace rosidl_typesupport_fastrtps_cpp
{

template<>
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_EXPORT_ri_seaweed_interfaces
const rosidl_message_type_support_t *
get_message_type_support_handle<ri_seaweed_interfaces::msg::Gripper>()
{
  return &ri_seaweed_interfaces::msg::typesupport_fastrtps_cpp::_Gripper__handle;
}

}  // namespace rosidl_typesupport_fastrtps_cpp

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, ri_seaweed_interfaces, msg, Gripper)() {
  return &ri_seaweed_interfaces::msg::typesupport_fastrtps_cpp::_Gripper__handle;
}

#ifdef __cplusplus
}
#endif
