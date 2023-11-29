// generated from rosidl_generator_py/resource/_idl_support.c.em
// with input from serial_motor_demo_msgs:msg/MotorCommand.idl
// generated code does not contain a copyright notice
#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include <Python.h>
#include <stdbool.h>
#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-function"
#endif
#include "numpy/ndarrayobject.h"
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif
#include "rosidl_runtime_c/visibility_control.h"
#include "serial_motor_demo_msgs/msg/detail/motor_command__struct.h"
#include "serial_motor_demo_msgs/msg/detail/motor_command__functions.h"


ROSIDL_GENERATOR_C_EXPORT
bool serial_motor_demo_msgs__msg__motor_command__convert_from_py(PyObject * _pymsg, void * _ros_message)
{
  // check that the passed message is of the expected Python class
  {
    char full_classname_dest[55];
    {
      char * class_name = NULL;
      char * module_name = NULL;
      {
        PyObject * class_attr = PyObject_GetAttrString(_pymsg, "__class__");
        if (class_attr) {
          PyObject * name_attr = PyObject_GetAttrString(class_attr, "__name__");
          if (name_attr) {
            class_name = (char *)PyUnicode_1BYTE_DATA(name_attr);
            Py_DECREF(name_attr);
          }
          PyObject * module_attr = PyObject_GetAttrString(class_attr, "__module__");
          if (module_attr) {
            module_name = (char *)PyUnicode_1BYTE_DATA(module_attr);
            Py_DECREF(module_attr);
          }
          Py_DECREF(class_attr);
        }
      }
      if (!class_name || !module_name) {
        return false;
      }
      snprintf(full_classname_dest, sizeof(full_classname_dest), "%s.%s", module_name, class_name);
    }
    assert(strncmp("serial_motor_demo_msgs.msg._motor_command.MotorCommand", full_classname_dest, 54) == 0);
  }
  serial_motor_demo_msgs__msg__MotorCommand * ros_message = _ros_message;
  {  // is_pwm
    PyObject * field = PyObject_GetAttrString(_pymsg, "is_pwm");
    if (!field) {
      return false;
    }
    assert(PyBool_Check(field));
    ros_message->is_pwm = (Py_True == field);
    Py_DECREF(field);
  }
  {  // mot_1_req_rad_sec
    PyObject * field = PyObject_GetAttrString(_pymsg, "mot_1_req_rad_sec");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->mot_1_req_rad_sec = (float)PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // mot_2_req_rad_sec
    PyObject * field = PyObject_GetAttrString(_pymsg, "mot_2_req_rad_sec");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->mot_2_req_rad_sec = (float)PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }

  return true;
}

ROSIDL_GENERATOR_C_EXPORT
PyObject * serial_motor_demo_msgs__msg__motor_command__convert_to_py(void * raw_ros_message)
{
  /* NOTE(esteve): Call constructor of MotorCommand */
  PyObject * _pymessage = NULL;
  {
    PyObject * pymessage_module = PyImport_ImportModule("serial_motor_demo_msgs.msg._motor_command");
    assert(pymessage_module);
    PyObject * pymessage_class = PyObject_GetAttrString(pymessage_module, "MotorCommand");
    assert(pymessage_class);
    Py_DECREF(pymessage_module);
    _pymessage = PyObject_CallObject(pymessage_class, NULL);
    Py_DECREF(pymessage_class);
    if (!_pymessage) {
      return NULL;
    }
  }
  serial_motor_demo_msgs__msg__MotorCommand * ros_message = (serial_motor_demo_msgs__msg__MotorCommand *)raw_ros_message;
  {  // is_pwm
    PyObject * field = NULL;
    field = PyBool_FromLong(ros_message->is_pwm ? 1 : 0);
    {
      int rc = PyObject_SetAttrString(_pymessage, "is_pwm", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // mot_1_req_rad_sec
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->mot_1_req_rad_sec);
    {
      int rc = PyObject_SetAttrString(_pymessage, "mot_1_req_rad_sec", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // mot_2_req_rad_sec
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->mot_2_req_rad_sec);
    {
      int rc = PyObject_SetAttrString(_pymessage, "mot_2_req_rad_sec", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }

  // ownership of _pymessage is transferred to the caller
  return _pymessage;
}
