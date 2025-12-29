cmake_minimum_required(VERSION 3.8)
project(demo_cpp_pkg)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)  # 直接查找 rclcpp 对应的头文件和库文件
# uncomment the following section in order to fill in
# further dependencies manually.
# find_package(<dependency> REQUIRED)

add_executable(cpp_node src/cpp_node.cpp)  # 添加可执行文件 add_executable(g++ 输出的目标文件(可执行文件)的名字 源程序的名字)
add_executable(person_node src/person_node.cpp)
add_executable(learn_auto src/learn_auto.cpp)
add_executable(learn_shared_ptr src/learn_shared_ptr.cpp)
add_executable(learn_lambda src/learn_lambda.cpp)

# message(STATUS ${rclcpp_INCLUDE_DIRS})  # 头文件及 rclcpp 依赖的头文件
# message(STATUS ${rclcpp_LIBRARIES})  # 库文件及 rclcpp 依赖的库文件

# target_include_directories(cpp_node PUBLIC ${rclcpp_INCLUDE_DIRS})  # 将“头文件及 rclcpp 依赖的头文件”包含到可执行文件

# target_link_libraries(cpp_node ${rclcpp_LIBRARIES})  # 将“库文件及 rclcpp 依赖的库文件”链接到可执行文件

ament_target_dependencies(cpp_node rclcpp)  # 代替上面两个命令
ament_target_dependencies(person_node rclcpp)
ament_target_dependencies(learn_auto rclcpp)
ament_target_dependencies(learn_shared_ptr rclcpp)
ament_target_dependencies(learn_lambda rclcpp)

install(TARGETS cpp_node           # 安装命令
  DESTINATION lib/${PROJECT_NAME}  # 拷贝可执行文件的目标地址
)

install(TARGETS person_node
  DESTINATION lib/${PROJECT_NAME}
)

install(TARGETS learn_auto
  DESTINATION lib/${PROJECT_NAME}
)

install(TARGETS learn_shared_ptr
  DESTINATION lib/${PROJECT_NAME}
)

install(TARGETS learn_lambda
  DESTINATION lib/${PROJECT_NAME}
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

ament_package()  # 代表 cmake 指令结束了
