# 安装 Gazebo
sudo apt install gazebo

# 下载模型
mkdir -p ~/.gazebo
cd ~/.gazebo
git clone https://gitee.com/zylyehuo/gazebo_models.git ~/.gazebo/models

# 删掉 .git 防止误识别为模型
rm -rf ~/.gazebo/models/.git

# 打开 gazebo
gazebo

# 安装 URDF 转换 sdf 插件
sudo apt install ros-$ROS_DISTRO-gazebo-ros-pkgs

# 通过 spawn_entity.py 将 URDF 转换为 sdf
# 然后调用相应的服务，把 sdf 加载到 gazebo 中
ros2 run gazebo_ros spawn_entity.py

# 安装并使用 robot_steering 来控制 /cmd_vel 话题
sudo apt update
sudo apt install ros-humble-rqt-robot-steering
ros2 run rqt_robot_steering rqt_robot_steering --force-discover