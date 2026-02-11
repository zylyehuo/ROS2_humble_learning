# 基于 ROS 2 和 Navigation 2 自动巡检机器人

## 1.项目介绍

本项目基于 ROS 2 和  Navigation 2 设计了一个自动巡检机器人仿真功能。

该巡检机器人要能够在不同的目标点之间进行循环移动，每到达一个目标点后首先通过语音播放到达的目标点信息，接着通过摄像头采集一张实时的图像并保存到本地。

各功能包功能如下：
- fishbot_description 机器人描述文件，包含仿真相关配置
- fishbot_navigation2 机器人导航配置文件
- fishbot_application 机器人导航应用 Python 代码
- fishbot_application_cpp 机器人导航应用 C++ 代码
- autopatrol_interfaces  自动巡检相关接口
- autopatrol_robot  自动巡检实现功能包

## 2.使用方法

本项目开发平台信息如下：

- 系统版本： Ubunt22.04
- ROS 版本：ROS 2 Humble

### 2.1安装

本项目建图采用 slam-toolbox，导航采用 Navigation 2 ,仿真采用 Gazebo，运动控制采用 ros2-control 实现，构建之前请先安装依赖，指令如下：

1. 安装 SLAM 和 Navigation 2

```
sudo apt install ros-$ROS_DISTRO-nav2-bringup ros-$ROS_DISTRO-slam-toolbox
```

2. 安装仿真相关功能包

```
sudo apt install ros-$ROS_DISTRO-robot-state-publisher  ros-$ROS_DISTRO-joint-state-publisher ros-$ROS_DISTRO-gazebo-ros-pkgs ros-$ROS_DISTRO-ros2-controllers ros-$ROS_DISTRO-xacro
```

3. 安装语音合成和图像相关功能包

```
sudo apt install python3-pip  -y
sudo apt install espeak-ng -y
sudo pip3 install espeakng
sudo apt install ros-$ROS_DISTRO-tf-transformations
sudo pip3 install transforms3d
```

### 2.2运行

安装完成依赖后，可以使用 colcon 工具进行构建和运行。

构建功能包

```
colcon build
```

运行仿真

```
source install/setup.bash
ros2 launch fishbot_description gazebo_sim.launch.py
```

运行导航

```
source install/setup.bash
ros2 launch fishbot_navigation2 navigation2.launch.py
```

运行自动巡检

```
source install/setup.bash
ros2 launch autopatrol_robot autopatrol.launch.py
```

## 3.作者

- [fishros](https://github.com/fishros)

# 7.1
## 将第六章 src 下的 robot_description2 复制到第七章的 src 下
sudo apt update
sudo apt install ros-humble-slam-toolbox

## 测试代码
ros2 launch robot_description2 gazebo_add_robot_add_joint_diff_controller_sim.launch.py
ros2 launch slam_toolbox online_async_launch.py use_sim_time:=True
rviz2
ros2 run teleop_twist_keyboard teleop_twist_keyboard

# 7.2
## 将地图保存为文件
sudo apt install ros-$ROS_DISTRO-nav2-map-server
ros2 run nav2_map_server map_saver_cli -f room
ros2 pkg create fishbot_navigation2

## 查看 .pgm 文件
sudo apt install eog
cd ~/ROS2_learning/chapter7/chapt7_ws/src/fishbot_navigation2/maps
eog room.pgm

# 7.3
## 安装 navigation2
sudo apt install ros-$ROS_DISTRO-navigation2
### 安装 navigation2 示例功能包
sudo apt install ros-$ROS_DISTRO-nav2-bringup
### 配置 navigation2 配置文件
cp /opt/ros/$ROS_DISTRO/share/nav2_bringup/params/nav2_params.yaml /home/zylyehuo/ROS2_learning/chapter7/chapt7_ws/src/fishbot_navigation2/config
ros2 launch fishbot_navigation2 navigation2.launch.py

# 7.4
## 查看定位信息
ros2 node info /amcl

## 发布初始位姿
cd ~/ROS2_learning/chapter7/chapt7_ws/
source install/setup.bash
ros2 run fishbot_application init_robot_pose

## 获取机器人位姿
cd ~/ROS2_learning/chapter7/chapt7_ws/
source install/setup.bash
ros2 run fishbot_application get_robot_pose --ros-args -p use_sim_time:=true

## 使用 action 机制发布目标位置
ros2 action send_goal /navigate_to_pose nav2_msgs/action/NavigateToPose "{pose: {header: {frame_id: map}, pose: {position: {x: 0.0, y: 0.0}}}}" --feedback

## 基于代码发布目标位置
cd ~/ROS2_learning/chapter7/chapt7_ws/
source install/setup.bash
ros2 run fishbot_application nav_to_pose

## 多点导航
ros2 interface show nav2_msgs/action/FollowWaypoints
cd ~/ROS2_learning/chapter7/chapt7_ws/
source install/setup.bash
ros2 run fishbot_application waypoints_follower

# 7.5
## 自动生成参数文件
cd ~/ROS2_learning/chapter7/chapt7_ws/
source install/setup.bash
ros2 run autopatrol_robot patrol_node
ros2 param dump /patrol_node

## 测试读取参数文件
ros2 run autopatrol_robot patrol_node --ros-args --params-file /home/zylyehuo/ROS2_learning/chapter7/chapt7_ws/install/autopatrol_robot/share/autopatrol_robot/config/patrol_config.yaml

## 测试合成语音播报
ros2 launch robot_description2 gazebo_add_robot_add_joint_diff_controller_sim.launch.py
ros2 launch fishbot_navigation2 navigation2.launch.py
ros2 launch autopatrol_robot autopatrol.launch.py

## 测试图像
ros2 launch robot_description2 gazebo_add_robot_add_joint_diff_controller_sim.launch.py
ros2 launch fishbot_navigation2 navigation2.launch.py
ros2 launch autopatrol_robot autopatrol_image.launch.py
