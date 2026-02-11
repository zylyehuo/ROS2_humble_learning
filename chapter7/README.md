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
