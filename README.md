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

* NOTE: Localization package( eg: nav2_amckl, slam_toolbox), will create map->odom transform

## **How to use**
 
  * Create a workspace and src directory inside the ws.
  * Navigate to the src directory and clone this repo.
  * come out of the directory and run:
  ```
    "colcon build --symlink-install" to build the package.
  ```
  * run:
  ```
    "source install/setup.bash" to source the built ws".
  ```
  * Execute following commands:
  ```
    ros2 launch dev_pi_communicate robot_bringup.launch.py 
  ```
  * Launch rplidar package:
  ```
    ros2 run rplidar_ros rplidar_composition --ros-args -p serial_port:=/dev/serial/by-id/usb-Silicon_Labs_CP2102_USB_to_UART_Bridge_Controller_0001-if00-port0 -p serial_baudrate:=115200 -p angle_compensate:=true -p frame_id:=laser_frame
  ```
  * To publish the saved map: 
  ```
    ros2 run nav2_map_server map_server --ros-args -p yaml_filename:=./ros-projects/dev_pi_communicate/new_map.yaml
  ```
  ```  
    ros2 run nav2_util lifecycle_bringup map_server 
  ```
  * To launch AMCL:
  ```  
    ros2 run nav2_amcl amcl --params-file ~/ros-projects/dev_pi_communicate/src/dev_pi_communicate/config/nav2_amcl.yaml 
  ```
  ```  
    ros2 run nav2_util lifecycle_bringup amcl
  ```
  * Launch nav2 navigation launch file:
  ```
    ros2 launch nav2_bringup navigation_launch.py params_file:=./ros-projects/dev_pi_communicate/src/dev_pi_communicate/config/ nav2_params.yaml
  ```
  * To launch EKF package:
  ```  
    ros2 launch robot_localization ekf.launch.py
  ```
  * To run laser filter node:
  ```
    ros2 run laser_filters scan_to_scan_filter_chain --ros-args --params-file /home/rpi/ros-projects/dev_pi_communicate/src/dev_pi_communicate/config/laser_filter.yaml
  ```
  * To run micro_ros client:
  ```  
    ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/serial/by-id/usb-Silicon_Labs_CP2102_USB_to_UART_Bridge_Controller_0001-if00-port0
  ```
  * To launch SLAM_TOOLBOX(To create new map)
  ```
    ros2 launch slam_toolbox online_async_launch.py slam_params_file:=./src/dev_pi_communicate/config/mapper_params_online_async.yaml 
  ```
  * To save the map: 
  ``` 
    ros2 run nav2_map_server map_saver_cli -f /filename
  ```
  

## ***Resources***

**Links**:
- https://docs.ros.org/en/humble/index.html
- https://github.com/SteveMacenski/slam_toolbox
- https://navigation.ros.org/

## Images

![MAP OF GAMEFEILD!](/docs/gamefield.png "map")


