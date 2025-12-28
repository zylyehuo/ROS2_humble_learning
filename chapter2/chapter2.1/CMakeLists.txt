cmake_minimum_required(VERSION 3.8)  # 设置 cmake 需要的最小版本

project(ros2_cpp)  # 配置工程的名字

add_executable(ros2_cpp_node ros2_cpp_node.cpp)  # 添加可执行文件 add_executable(g++ 输出的目标文件(可执行文件)的名字 源程序的名字)

find_package(rclcpp REQUIRED)  # 直接查找 rclcpp 对应的头文件和库文件

target_include_directories(ros2_cpp_node PUBLIC ${rclcpp_INCLUDE_DIRS})  # 将“头文件及 rclcpp 依赖的头文件”包含到可执行文件

target_link_libraries(ros2_cpp_node ${rclcpp_LIBRARIES})  # 将“库文件及 rclcpp 依赖的库文件”链接到可执行文件