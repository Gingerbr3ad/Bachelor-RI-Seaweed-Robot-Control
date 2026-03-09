// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from ri_seaweed_interfaces:msg/Gripper.idl
// generated code does not contain a copyright notice
#include "ri_seaweed_interfaces/msg/detail/gripper__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


bool
ri_seaweed_interfaces__msg__Gripper__init(ri_seaweed_interfaces__msg__Gripper * msg)
{
  if (!msg) {
    return false;
  }
  // gripper_state
  // close_request
  return true;
}

void
ri_seaweed_interfaces__msg__Gripper__fini(ri_seaweed_interfaces__msg__Gripper * msg)
{
  if (!msg) {
    return;
  }
  // gripper_state
  // close_request
}

bool
ri_seaweed_interfaces__msg__Gripper__are_equal(const ri_seaweed_interfaces__msg__Gripper * lhs, const ri_seaweed_interfaces__msg__Gripper * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // gripper_state
  if (lhs->gripper_state != rhs->gripper_state) {
    return false;
  }
  // close_request
  if (lhs->close_request != rhs->close_request) {
    return false;
  }
  return true;
}

bool
ri_seaweed_interfaces__msg__Gripper__copy(
  const ri_seaweed_interfaces__msg__Gripper * input,
  ri_seaweed_interfaces__msg__Gripper * output)
{
  if (!input || !output) {
    return false;
  }
  // gripper_state
  output->gripper_state = input->gripper_state;
  // close_request
  output->close_request = input->close_request;
  return true;
}

ri_seaweed_interfaces__msg__Gripper *
ri_seaweed_interfaces__msg__Gripper__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  ri_seaweed_interfaces__msg__Gripper * msg = (ri_seaweed_interfaces__msg__Gripper *)allocator.allocate(sizeof(ri_seaweed_interfaces__msg__Gripper), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(ri_seaweed_interfaces__msg__Gripper));
  bool success = ri_seaweed_interfaces__msg__Gripper__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
ri_seaweed_interfaces__msg__Gripper__destroy(ri_seaweed_interfaces__msg__Gripper * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    ri_seaweed_interfaces__msg__Gripper__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
ri_seaweed_interfaces__msg__Gripper__Sequence__init(ri_seaweed_interfaces__msg__Gripper__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  ri_seaweed_interfaces__msg__Gripper * data = NULL;

  if (size) {
    data = (ri_seaweed_interfaces__msg__Gripper *)allocator.zero_allocate(size, sizeof(ri_seaweed_interfaces__msg__Gripper), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = ri_seaweed_interfaces__msg__Gripper__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        ri_seaweed_interfaces__msg__Gripper__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
ri_seaweed_interfaces__msg__Gripper__Sequence__fini(ri_seaweed_interfaces__msg__Gripper__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      ri_seaweed_interfaces__msg__Gripper__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

ri_seaweed_interfaces__msg__Gripper__Sequence *
ri_seaweed_interfaces__msg__Gripper__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  ri_seaweed_interfaces__msg__Gripper__Sequence * array = (ri_seaweed_interfaces__msg__Gripper__Sequence *)allocator.allocate(sizeof(ri_seaweed_interfaces__msg__Gripper__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = ri_seaweed_interfaces__msg__Gripper__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
ri_seaweed_interfaces__msg__Gripper__Sequence__destroy(ri_seaweed_interfaces__msg__Gripper__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    ri_seaweed_interfaces__msg__Gripper__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
ri_seaweed_interfaces__msg__Gripper__Sequence__are_equal(const ri_seaweed_interfaces__msg__Gripper__Sequence * lhs, const ri_seaweed_interfaces__msg__Gripper__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!ri_seaweed_interfaces__msg__Gripper__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
ri_seaweed_interfaces__msg__Gripper__Sequence__copy(
  const ri_seaweed_interfaces__msg__Gripper__Sequence * input,
  ri_seaweed_interfaces__msg__Gripper__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(ri_seaweed_interfaces__msg__Gripper);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    ri_seaweed_interfaces__msg__Gripper * data =
      (ri_seaweed_interfaces__msg__Gripper *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!ri_seaweed_interfaces__msg__Gripper__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          ri_seaweed_interfaces__msg__Gripper__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!ri_seaweed_interfaces__msg__Gripper__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
