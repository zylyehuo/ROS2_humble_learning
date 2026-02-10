# 将第六章 src 下的 robot_description2 复制到第七章的 src 下
sudo apt update
sudo apt install ros-humble-slam-toolbox

# 测试代码
ros2 launch robot_description2 gazebo_add_robot_add_joint_diff_controller_sim.launch.py
ros2 launch slam_toolbox online_async_launch.py use_sim_time:=True
rviz2
ros2 run teleop_twist_keyboard teleop_twist_keyboard

# 将地图保存为文件
sudo apt install ros-$ROS_DISTRO-nav2-map-server
ros2 run nav2_map_server map_saver_cli -f room
ros2 pkg create fishbot_navigation2

# 查看 .pgm 文件
sudo apt install eog
cd ~/ROS2_learning/chapter7/chapt7_ws/src/fishbot_navigation2/maps
eog room.pgm

# 安装 navigation2
sudo apt install ros-$ROS_DISTRO-navigation2
## 安装 navigation2 示例功能包
sudo apt install ros-$ROS_DISTRO-nav2-bringup
## 配置 navigation2 配置文件
cp /opt/ros/$ROS_DISTRO/share/nav2_bringup/params/nav2_params.yaml /home/zylyehuo/ROS2_learning/chapter7/chapt7_ws/src/fishbot_navigation2/config
