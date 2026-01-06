# 安装 ros2_control
sudo apt install ros-$ROS_DISTRO-ros2-control

# 检查是否安装成功
ros2 control --help

# 查看有哪些传感器
sudo apt info ros-$ROS_DISTRO-ros2-controllers

# 安装 ros2_control 提供的控制器
sudo apt install ros-$ROS_DISTRO-ros2-controllers

# 安装 Gazebo 中使用的 ros2_control 插件
sudo apt install ros-$ROS_DISTRO-gazebo-ros2-control