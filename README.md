# DEV_PI_COMMUNICATE

--- 

## **Introduction**

This is a ROS2 package for controlling our robot. It contains multiple nodes and topics.
The executables and transforms are listed as follows:

* **Executables:**
1. joy_node: To receive the data from joystick controller and generate the necessary command for stm32
2. camera_node: To receive the data from camera and generate the necessary command for stm32
3. serial_comm_node: To recieve data from stm32 serially
4. teleop_key_node: To control the bot from teleop_twist_keyboard
5. publisher_node: practice node for publishing immediate data
5. subscriber_node: practice node for receiving immediate data

* **Transforms:**
1. map->base_link
2. odom->base_link
3. base_link->laser_frame  
  (If you launch slam_toolbox package, it will create map->odom transform)

## **How to use**
 
 * Create a workspace and src directory inside the ws.
 * Navigate to the src directory and clone this repo.
 * come out of the directory and run: "colcon build --symlink-install" to build the package.
 * run: "source install/local_install.bash" to source the built ws".
 * Execute following commands:
    * ros2 launch dev_pi_communicate robot_bringup.launch.py 
    * ros2 launch slam_toolbox online_async_launch.py slam_params_file:=./src/dev_pi_communicate/config/mapper_params_online_async.yaml 
    * ros2 launch nav2_bringup navigation_launch.py
    * To save the map: 
      - ros2 run nav2_map_server map_saver_cli -f /filename
    * To publishe the saved map: 
      - ros2 run nav2_map_server map_server --ros-args -p yaml_filename:=/mapper.yaml
      - ros2 run nav2_util lifecycle_bringup map_server -> this will configure the inactive node (map_server) to active state
      
    * To run micro_ros client:
      - ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/serial/by-id/usb-Silicon_Labs_CP2102_USB_to_UART_Bridge_Controller_0001-if00-port0

## ***Resources***

**Links**:
- https://docs.ros.org/en/humble/index.html
- https://github.com/SteveMacenski/slam_toolbox
- https://navigation.ros.org/

## Images

![FIRST MAP OF GAMEFEILD!](/docs/Screenshot%20from%202023-12-21%2014-33-36.png "map")


