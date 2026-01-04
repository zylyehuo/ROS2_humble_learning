# 发布 base_link 到 base_laser 的静态坐标转换
ros2 run tf2_ros static_transform_publisher --x 0.1 --y 0.0 --z 0.2 --roll 0.0 --pitch 0.0 --yaw 0.0 --frame-id base_link --child-frame-id base_laser

# 发布 base_laser 到 wall_point 的静态坐标转换
ros2 run tf2_ros static_transform_publisher --x 0.3 --y 0.0 --z 0.0 --roll 0.0 --pitch 0.0 --yaw 0.0 --frame-id base_laser --child-frame-id wall_point

# 查询 base_link 到 wall_point 之间的关系
ros2 run tf2_ros tf2_echo base_link wall_point

# 安装工具
sudo apt install ros-humble-mrpt-apps
3d-rotation-converter

# 使用命令行查看 TF 数
ros2 run tf2_tools view_frames

# 安装 ROS 坐标变换工具 
sudo apt install ros-$ROS_DISTRO-tf-transformations

# 安装 Python 坐标变换工具(欧拉角转换为四元数) 
pip3 install transforms3d 
