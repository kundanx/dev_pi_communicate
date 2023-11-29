// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from serial_motor_demo_msgs:msg/EncoderVals.idl
// generated code does not contain a copyright notice
#include "serial_motor_demo_msgs/msg/detail/encoder_vals__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


bool
serial_motor_demo_msgs__msg__EncoderVals__init(serial_motor_demo_msgs__msg__EncoderVals * msg)
{
  if (!msg) {
    return false;
  }
  // mot_1_enc_val
  // mot_2_enc_val
  return true;
}

void
serial_motor_demo_msgs__msg__EncoderVals__fini(serial_motor_demo_msgs__msg__EncoderVals * msg)
{
  if (!msg) {
    return;
  }
  // mot_1_enc_val
  // mot_2_enc_val
}

bool
serial_motor_demo_msgs__msg__EncoderVals__are_equal(const serial_motor_demo_msgs__msg__EncoderVals * lhs, const serial_motor_demo_msgs__msg__EncoderVals * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // mot_1_enc_val
  if (lhs->mot_1_enc_val != rhs->mot_1_enc_val) {
    return false;
  }
  // mot_2_enc_val
  if (lhs->mot_2_enc_val != rhs->mot_2_enc_val) {
    return false;
  }
  return true;
}

bool
serial_motor_demo_msgs__msg__EncoderVals__copy(
  const serial_motor_demo_msgs__msg__EncoderVals * input,
  serial_motor_demo_msgs__msg__EncoderVals * output)
{
  if (!input || !output) {
    return false;
  }
  // mot_1_enc_val
  output->mot_1_enc_val = input->mot_1_enc_val;
  // mot_2_enc_val
  output->mot_2_enc_val = input->mot_2_enc_val;
  return true;
}

serial_motor_demo_msgs__msg__EncoderVals *
serial_motor_demo_msgs__msg__EncoderVals__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  serial_motor_demo_msgs__msg__EncoderVals * msg = (serial_motor_demo_msgs__msg__EncoderVals *)allocator.allocate(sizeof(serial_motor_demo_msgs__msg__EncoderVals), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(serial_motor_demo_msgs__msg__EncoderVals));
  bool success = serial_motor_demo_msgs__msg__EncoderVals__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
serial_motor_demo_msgs__msg__EncoderVals__destroy(serial_motor_demo_msgs__msg__EncoderVals * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    serial_motor_demo_msgs__msg__EncoderVals__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
serial_motor_demo_msgs__msg__EncoderVals__Sequence__init(serial_motor_demo_msgs__msg__EncoderVals__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  serial_motor_demo_msgs__msg__EncoderVals * data = NULL;

  if (size) {
    data = (serial_motor_demo_msgs__msg__EncoderVals *)allocator.zero_allocate(size, sizeof(serial_motor_demo_msgs__msg__EncoderVals), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = serial_motor_demo_msgs__msg__EncoderVals__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        serial_motor_demo_msgs__msg__EncoderVals__fini(&data[i - 1]);
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
serial_motor_demo_msgs__msg__EncoderVals__Sequence__fini(serial_motor_demo_msgs__msg__EncoderVals__Sequence * array)
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
      serial_motor_demo_msgs__msg__EncoderVals__fini(&array->data[i]);
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

serial_motor_demo_msgs__msg__EncoderVals__Sequence *
serial_motor_demo_msgs__msg__EncoderVals__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  serial_motor_demo_msgs__msg__EncoderVals__Sequence * array = (serial_motor_demo_msgs__msg__EncoderVals__Sequence *)allocator.allocate(sizeof(serial_motor_demo_msgs__msg__EncoderVals__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = serial_motor_demo_msgs__msg__EncoderVals__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
serial_motor_demo_msgs__msg__EncoderVals__Sequence__destroy(serial_motor_demo_msgs__msg__EncoderVals__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    serial_motor_demo_msgs__msg__EncoderVals__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
serial_motor_demo_msgs__msg__EncoderVals__Sequence__are_equal(const serial_motor_demo_msgs__msg__EncoderVals__Sequence * lhs, const serial_motor_demo_msgs__msg__EncoderVals__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!serial_motor_demo_msgs__msg__EncoderVals__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
serial_motor_demo_msgs__msg__EncoderVals__Sequence__copy(
  const serial_motor_demo_msgs__msg__EncoderVals__Sequence * input,
  serial_motor_demo_msgs__msg__EncoderVals__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(serial_motor_demo_msgs__msg__EncoderVals);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    serial_motor_demo_msgs__msg__EncoderVals * data =
      (serial_motor_demo_msgs__msg__EncoderVals *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!serial_motor_demo_msgs__msg__EncoderVals__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          serial_motor_demo_msgs__msg__EncoderVals__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!serial_motor_demo_msgs__msg__EncoderVals__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
