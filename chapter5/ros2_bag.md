# 运行节点
ros2 run turtlesim turtlesim_node
ros2 run turtlesim turtle_teleop_key

# 查看话题
ros2 topic list

# 记录
ros2 bag record /turtle1/cmd_vel

# 播放【使用文件夹名字】
ros2 bag play rosbag2_XXXX_XX_XX-XX_XXXX_XX/