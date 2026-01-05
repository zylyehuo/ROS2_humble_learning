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