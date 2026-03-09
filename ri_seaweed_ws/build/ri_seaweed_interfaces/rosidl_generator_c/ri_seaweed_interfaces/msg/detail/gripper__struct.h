// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from ri_seaweed_interfaces:msg/Gripper.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "ri_seaweed_interfaces/msg/gripper.h"


#ifndef RI_SEAWEED_INTERFACES__MSG__DETAIL__GRIPPER__STRUCT_H_
#define RI_SEAWEED_INTERFACES__MSG__DETAIL__GRIPPER__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

// Constants defined in the message

/// Struct defined in msg/Gripper in the package ri_seaweed_interfaces.
typedef struct ri_seaweed_interfaces__msg__Gripper
{
  bool gripper_state;
  bool close_request;
} ri_seaweed_interfaces__msg__Gripper;

// Struct for a sequence of ri_seaweed_interfaces__msg__Gripper.
typedef struct ri_seaweed_interfaces__msg__Gripper__Sequence
{
  ri_seaweed_interfaces__msg__Gripper * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} ri_seaweed_interfaces__msg__Gripper__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // RI_SEAWEED_INTERFACES__MSG__DETAIL__GRIPPER__STRUCT_H_
