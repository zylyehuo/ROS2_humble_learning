# 8.1
## 8.1.1
### 安装 pluginlib，是用于在 ROS 功能包中动态加载和卸载插件的 C++ 库
```
sudo apt install ros-$ROS_DISTRO-pluginlib -y
```

## 8.1.2
```
ros2 pkg create motion_control_system --dependencies pluginlib --license Apache-2.0
```

## 8.1.4
```
ros2 run motion_control_system test_plugin motion_control_system/SpinMotionController
```
### 查看可执行文件链接了哪些库
```
cd /home/zylyehuo/ROS2_learning/chapter8/chapt8_ws/install/motion_control_system/lib/motion_control_system
ldd test_plugin
```

# 8.2
## 8.2.1
### 查看位置接口
```
ros2 interface show geometry_msgs/msg/PoseStamped
```
### 查看栅格地图接口
```
ros2 interface show nav_msgs/msg/OccupancyGrid
```
### 查看路径接口
```
ros2 interface show nav_msgs/msg/Path
```
## 8.2.2
```
cd /home/zylyehuo/ROS2_learning/chapter8/chapt8_ws2
```
> 将第七章的功能包复制过来
```
cp -r ../../chapter7/chapt7_ws/src/ .
```
```
ros2 pkg create nav2_custom_planner --dependencies pluginlib nav2_core --license Apache-2.0
```
## 8.2.4
```
cd ~/ROS2_learning/chapter8/chapt8_ws2/
source install/setup.bash
ros2 launch robot_description2 gazebo_add_robot_add_joint_diff_controller_sim.launch.py
```
```
cd ~/ROS2_learning/chapter8/chapt8_ws2/
source install/setup.bash
ros2 launch fishbot_navigation2 navigation2.launch.py
```

# 8.3
## 8.3.2
```
cd ~/ROS2_learning/chapter8/chapt8_ws2/src
ros2 pkg create nav2_custom_controller --build-type ament_cmake --dependencies pluginlib nav2_core --license Apache-2.0
```
## 8.3.4
```
cd ~/ROS2_learning/chapter8/chapt8_ws2/
source install/setup.bash
ros2 launch robot_description2 gazebo_add_robot_add_joint_diff_controller_sim.launch.py
```
```
cd ~/ROS2_learning/chapter8/chapt8_ws2/
source install/setup.bash
ros2 launch fishbot_navigation2 navigation2.launch.py
```