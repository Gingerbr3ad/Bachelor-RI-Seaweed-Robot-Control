// generated from rosidl_typesupport_fastrtps_c/resource/idl__rosidl_typesupport_fastrtps_c.h.em
// with input from ri_seaweed_interfaces:msg/Gripper.idl
// generated code does not contain a copyright notice
#ifndef RI_SEAWEED_INTERFACES__MSG__DETAIL__GRIPPER__ROSIDL_TYPESUPPORT_FASTRTPS_C_H_
#define RI_SEAWEED_INTERFACES__MSG__DETAIL__GRIPPER__ROSIDL_TYPESUPPORT_FASTRTPS_C_H_


#include <stddef.h>
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_interface/macros.h"
#include "ri_seaweed_interfaces/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "ri_seaweed_interfaces/msg/detail/gripper__struct.h"
#include "fastcdr/Cdr.h"

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_ri_seaweed_interfaces
bool cdr_serialize_ri_seaweed_interfaces__msg__Gripper(
  const ri_seaweed_interfaces__msg__Gripper * ros_message,
  eprosima::fastcdr::Cdr & cdr);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_ri_seaweed_interfaces
bool cdr_deserialize_ri_seaweed_interfaces__msg__Gripper(
  eprosima::fastcdr::Cdr &,
  ri_seaweed_interfaces__msg__Gripper * ros_message);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_ri_seaweed_interfaces
size_t get_serialized_size_ri_seaweed_interfaces__msg__Gripper(
  const void * untyped_ros_message,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_ri_seaweed_interfaces
size_t max_serialized_size_ri_seaweed_interfaces__msg__Gripper(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_ri_seaweed_interfaces
bool cdr_serialize_key_ri_seaweed_interfaces__msg__Gripper(
  const ri_seaweed_interfaces__msg__Gripper * ros_message,
  eprosima::fastcdr::Cdr & cdr);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_ri_seaweed_interfaces
size_t get_serialized_size_key_ri_seaweed_interfaces__msg__Gripper(
  const void * untyped_ros_message,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_ri_seaweed_interfaces
size_t max_serialized_size_key_ri_seaweed_interfaces__msg__Gripper(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_ri_seaweed_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, ri_seaweed_interfaces, msg, Gripper)();

#ifdef __cplusplus
}
#endif

#endif  // RI_SEAWEED_INTERFACES__MSG__DETAIL__GRIPPER__ROSIDL_TYPESUPPORT_FASTRTPS_C_H_
