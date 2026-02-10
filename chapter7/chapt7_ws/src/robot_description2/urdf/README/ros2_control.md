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

# 查看控制器类型
ros2 control list_controller_types

# 列出硬件接口
ros2 control list_hardware_interfaces

# 列出所有的硬件组件
ros2 control list_hardware_components

# 发布控制器中关节的 TF 信息
ros2 control load_controller robot_joint_state_broadcaster --set-state active
# ros2 control load_controller robot_joint_state_broadcaster --set-state inactive

# 查看已经加载的控制器
ros2 control list_controllers

# 卸载控制器
ros2 control unload_controller robot_joint_state_broadcaster

# 查看“力控”控制器话题是否发布
ros2 topic list -t | grep effort

# 基于“力控”控制器发布控制命令
ros2 topic pub /robot_effort_controller/commands std_msgs/msg/Float64MultiArray "{data: [0.0001, 0.0001]}"

# 查看“差速”控制器话题是否发布
ros2 topic list -t | grep diff

# 基于“差速”控制器发布控制命令 /cmd_vel
ros2 run rqt_robot_steering rqt_robot_steering --force-discover
