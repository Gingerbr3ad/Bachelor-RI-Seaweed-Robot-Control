// generated from rosidl_generator_c/resource/idl__description.c.em
// with input from ri_seaweed_interfaces:msg/Gripper.idl
// generated code does not contain a copyright notice

#include "ri_seaweed_interfaces/msg/detail/gripper__functions.h"

ROSIDL_GENERATOR_C_PUBLIC_ri_seaweed_interfaces
const rosidl_type_hash_t *
ri_seaweed_interfaces__msg__Gripper__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0x5e, 0x4f, 0xd7, 0x6c, 0x33, 0x27, 0xc4, 0x7c,
      0xf3, 0x81, 0xf9, 0xf7, 0xd2, 0xea, 0xd5, 0x57,
      0x9e, 0x69, 0x4c, 0x47, 0x72, 0x60, 0xb0, 0xac,
      0x47, 0xd6, 0x9d, 0x47, 0x97, 0x97, 0xcc, 0x31,
    }};
  return &hash;
}

#include <assert.h>
#include <string.h>

// Include directives for referenced types

// Hashes for external referenced types
#ifndef NDEBUG
#endif

static char ri_seaweed_interfaces__msg__Gripper__TYPE_NAME[] = "ri_seaweed_interfaces/msg/Gripper";

// Define type names, field names, and default values
static char ri_seaweed_interfaces__msg__Gripper__FIELD_NAME__gripper_state[] = "gripper_state";
static char ri_seaweed_interfaces__msg__Gripper__FIELD_NAME__close_request[] = "close_request";

static rosidl_runtime_c__type_description__Field ri_seaweed_interfaces__msg__Gripper__FIELDS[] = {
  {
    {ri_seaweed_interfaces__msg__Gripper__FIELD_NAME__gripper_state, 13, 13},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_BOOLEAN,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {ri_seaweed_interfaces__msg__Gripper__FIELD_NAME__close_request, 13, 13},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_BOOLEAN,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
};

const rosidl_runtime_c__type_description__TypeDescription *
ri_seaweed_interfaces__msg__Gripper__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {ri_seaweed_interfaces__msg__Gripper__TYPE_NAME, 33, 33},
      {ri_seaweed_interfaces__msg__Gripper__FIELDS, 2, 2},
    },
    {NULL, 0, 0},
  };
  if (!constructed) {
    constructed = true;
  }
  return &description;
}

static char toplevel_type_raw_source[] =
  "bool gripper_state\n"
  "bool close_request";

static char msg_encoding[] = "msg";

// Define all individual source functions

const rosidl_runtime_c__type_description__TypeSource *
ri_seaweed_interfaces__msg__Gripper__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {ri_seaweed_interfaces__msg__Gripper__TYPE_NAME, 33, 33},
    {msg_encoding, 3, 3},
    {toplevel_type_raw_source, 37, 37},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
ri_seaweed_interfaces__msg__Gripper__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[1];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 1, 1};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *ri_seaweed_interfaces__msg__Gripper__get_individual_type_description_source(NULL),
    constructed = true;
  }
  return &source_sequence;
}
