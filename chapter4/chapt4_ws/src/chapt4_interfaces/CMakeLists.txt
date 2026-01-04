cmake_minimum_required(VERSION 3.8)
project(chapt4_interfaces)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(rosidl_default_generators REQUIRED)

# cmake 函数，来自于 rosidl_default_generators，用于将 msg 等消息接口定义文件转换成库或头文件类
rosidl_generate_interfaces(${PROJECT_NAME}
  "srv/FaceDetector.srv"  # 消息接口的相对路径
  "srv/Patrol.srv"
  DEPENDENCIES sensor_msgs  # 添加消息接口中所需要的依赖
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # comment the line when a copyright and license is added to all source files
  set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # comment the line when this package is in a git repo and when
  # a copyright and license is added to all source files
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
