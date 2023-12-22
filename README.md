# DEV_PI_COMMUNICATE
..
## **Introduction**

This is a ROS2 package for controlling our robot. It contains multiple nodes and topics.
The executables and transforms are listed as follows:

* **Executables:**
    joy_node: To receive the data from joystick controller and generate the necessary command for stm32
    camera_node: To receive the data from camera and generate the necessary command for stm32
    serial_comm_node: To recieve data from stm32 serially
    teleop_key_node: To control the bot from teleop_twist_keyboard
    publisher_node: practice node for publishing immediate data
    subscriber_node: practice node for receiving immediate data

* **Transforms:**
    map->base_link
    odom->base_link
    base_link->laser_frame
    (If you launch slam_toolbox package, it will create map->odom transform)

## **How to use**
 
 * Create a workspace and src directory inside the ws.
 * Navigate to the src directory and clone this repo.
 * come out of the directory and run: "colcon build --symlink-install" to build the package.
 * run: "source install/local_install.bash" to source the built ws".
 * Execute following commands:
    * ros2 launch dev_pi_communicate robot_bringup.launch.py 
    * ros2 launch slam_toolbox online_async_launch.py slam_params_file:=./src/dev_pi_communicate/parameter_files/mapper_params_online_async.yaml 

## ***Resources***

**Links**:
- https://docs.ros.org/en/humble/index.html
- https://github.com/SteveMacenski/slam_toolbox
- https://navigation.ros.org/


