cmake_minimum_required(VERSION 3.8)
project(nav2_custom_planner)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(pluginlib REQUIRED)
find_package(nav2_core REQUIRED)

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

# ================生成动态链接库，添加库文件=====================
include_directories(include)  # 添加头文件目录
set(library_name ${PROJECT_NAME}_plugin)  # 定义库名称
add_library(${library_name} SHARED  src/nav2_custom_planner.cpp)  # SHARED：添加动态链接库，
                                                                   # add_library(要生成的动态链接库的名字 SHARED 对应的源文件)
ament_target_dependencies(${library_name} nav2_core pluginlib)  # ament_target_dependencies(要生成的动态链接库的名字  需要的依赖)

# 将生成的动态链接库拷贝到 install 目录下
install(TARGETS ${library_name}
  ARCHIVE DESTINATION lib
  LIBRARY DESTINATION lib
  RUNTIME DESTINATION lib/${PROJECT_NAME}
)

# 将头文件所在目录拷贝到 install 目录下
install(DIRECTORY include/
  DESTINATION include/
)

# 导出插件描述文件
pluginlib_export_plugin_description_file(nav2_core custom_planner_plugin.xml)  # pluginlib_export_plugin_description_file(插件基类（接口）所在功能包的名字 插件描述文件的路径)

# ================生成动态链接库，添加库文件=====================

ament_package()
