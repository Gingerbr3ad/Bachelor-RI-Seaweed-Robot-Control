// generated from rosidl_generator_c/resource/idl__functions.h.em
// with input from ri_seaweed_interfaces:msg/Gripper.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "ri_seaweed_interfaces/msg/gripper.h"


#ifndef RI_SEAWEED_INTERFACES__MSG__DETAIL__GRIPPER__FUNCTIONS_H_
#define RI_SEAWEED_INTERFACES__MSG__DETAIL__GRIPPER__FUNCTIONS_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stdlib.h>

#include "rosidl_runtime_c/action_type_support_struct.h"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_runtime_c/service_type_support_struct.h"
#include "rosidl_runtime_c/type_description/type_description__struct.h"
#include "rosidl_runtime_c/type_description/type_source__struct.h"
#include "rosidl_runtime_c/type_hash.h"
#include "rosidl_runtime_c/visibility_control.h"
#include "ri_seaweed_interfaces/msg/rosidl_generator_c__visibility_control.h"

#include "ri_seaweed_interfaces/msg/detail/gripper__struct.h"

/// Initialize msg/Gripper message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * ri_seaweed_interfaces__msg__Gripper
 * )) before or use
 * ri_seaweed_interfaces__msg__Gripper__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_ri_seaweed_interfaces
bool
ri_seaweed_interfaces__msg__Gripper__init(ri_seaweed_interfaces__msg__Gripper * msg);

/// Finalize msg/Gripper message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_ri_seaweed_interfaces
void
ri_seaweed_interfaces__msg__Gripper__fini(ri_seaweed_interfaces__msg__Gripper * msg);

/// Create msg/Gripper message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * ri_seaweed_interfaces__msg__Gripper__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_ri_seaweed_interfaces
ri_seaweed_interfaces__msg__Gripper *
ri_seaweed_interfaces__msg__Gripper__create(void);

/// Destroy msg/Gripper message.
/**
 * It calls
 * ri_seaweed_interfaces__msg__Gripper__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_ri_seaweed_interfaces
void
ri_seaweed_interfaces__msg__Gripper__destroy(ri_seaweed_interfaces__msg__Gripper * msg);

/// Check for msg/Gripper message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_ri_seaweed_interfaces
bool
ri_seaweed_interfaces__msg__Gripper__are_equal(const ri_seaweed_interfaces__msg__Gripper * lhs, const ri_seaweed_interfaces__msg__Gripper * rhs);

/// Copy a msg/Gripper message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_ri_seaweed_interfaces
bool
ri_seaweed_interfaces__msg__Gripper__copy(
  const ri_seaweed_interfaces__msg__Gripper * input,
  ri_seaweed_interfaces__msg__Gripper * output);

/// Retrieve pointer to the hash of the description of this type.
ROSIDL_GENERATOR_C_PUBLIC_ri_seaweed_interfaces
const rosidl_type_hash_t *
ri_seaweed_interfaces__msg__Gripper__get_type_hash(
  const rosidl_message_type_support_t * type_support);

/// Retrieve pointer to the description of this type.
ROSIDL_GENERATOR_C_PUBLIC_ri_seaweed_interfaces
const rosidl_runtime_c__type_description__TypeDescription *
ri_seaweed_interfaces__msg__Gripper__get_type_description(
  const rosidl_message_type_support_t * type_support);

/// Retrieve pointer to the single raw source text that defined this type.
ROSIDL_GENERATOR_C_PUBLIC_ri_seaweed_interfaces
const rosidl_runtime_c__type_description__TypeSource *
ri_seaweed_interfaces__msg__Gripper__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support);

/// Retrieve pointer to the recursive raw sources that defined the description of this type.
ROSIDL_GENERATOR_C_PUBLIC_ri_seaweed_interfaces
const rosidl_runtime_c__type_description__TypeSource__Sequence *
ri_seaweed_interfaces__msg__Gripper__get_type_description_sources(
  const rosidl_message_type_support_t * type_support);

/// Initialize array of msg/Gripper messages.
/**
 * It allocates the memory for the number of elements and calls
 * ri_seaweed_interfaces__msg__Gripper__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_ri_seaweed_interfaces
bool
ri_seaweed_interfaces__msg__Gripper__Sequence__init(ri_seaweed_interfaces__msg__Gripper__Sequence * array, size_t size);

/// Finalize array of msg/Gripper messages.
/**
 * It calls
 * ri_seaweed_interfaces__msg__Gripper__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_ri_seaweed_interfaces
void
ri_seaweed_interfaces__msg__Gripper__Sequence__fini(ri_seaweed_interfaces__msg__Gripper__Sequence * array);

/// Create array of msg/Gripper messages.
/**
 * It allocates the memory for the array and calls
 * ri_seaweed_interfaces__msg__Gripper__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_ri_seaweed_interfaces
ri_seaweed_interfaces__msg__Gripper__Sequence *
ri_seaweed_interfaces__msg__Gripper__Sequence__create(size_t size);

/// Destroy array of msg/Gripper messages.
/**
 * It calls
 * ri_seaweed_interfaces__msg__Gripper__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_ri_seaweed_interfaces
void
ri_seaweed_interfaces__msg__Gripper__Sequence__destroy(ri_seaweed_interfaces__msg__Gripper__Sequence * array);

/// Check for msg/Gripper message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_ri_seaweed_interfaces
bool
ri_seaweed_interfaces__msg__Gripper__Sequence__are_equal(const ri_seaweed_interfaces__msg__Gripper__Sequence * lhs, const ri_seaweed_interfaces__msg__Gripper__Sequence * rhs);

/// Copy an array of msg/Gripper messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_ri_seaweed_interfaces
bool
ri_seaweed_interfaces__msg__Gripper__Sequence__copy(
  const ri_seaweed_interfaces__msg__Gripper__Sequence * input,
  ri_seaweed_interfaces__msg__Gripper__Sequence * output);

#ifdef __cplusplus
}
#endif

#endif  // RI_SEAWEED_INTERFACES__MSG__DETAIL__GRIPPER__FUNCTIONS_H_
