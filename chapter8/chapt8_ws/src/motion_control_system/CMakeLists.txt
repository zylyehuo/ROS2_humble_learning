cmake_minimum_required(VERSION 3.8)
project(motion_control_system)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(pluginlib REQUIRED)

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
add_library(spin_motion_controller SHARED src/spin_motion_controller.cpp)  # SHARED：添加动态链接库，
                                                                           # add_library(要生成的动态链接库的名字 SHARED 对应的源文件)
ament_target_dependencies(spin_motion_controller  pluginlib)  # ament_target_dependencies(要生成的动态链接库的名字  需要的依赖)

# 将生成的动态链接库拷贝到 install 目录下
install(TARGETS spin_motion_controller
  ARCHIVE DESTINATION lib
  LIBRARY DESTINATION lib
  RUNTIME DESTINATION bin
)

# 将头文件所在目录拷贝到 install 目录下
install(DIRECTORY include/
  DESTINATION include/
)

# 导出插件描述文件
pluginlib_export_plugin_description_file(motion_control_system spin_motion_plugins.xml)  # pluginlib_export_plugin_description_file(插件基类（接口）所在功能包的名字 插件描述文件的路径)

# ================生成动态链接库，添加库文件=====================

add_executable(test_plugin src/test_plugin.cpp)  # 添加可执行文件
ament_target_dependencies(test_plugin pluginlib)  # 添加依赖，不需要在链接阶段显式地声明需要依赖哪个动态链接库（spin_motion_controller）
                                                  # 通过动态链接库的名字（motion_control_system/SpinMotionController）找到动态链接库
                                                  # 通过动态链接库找到锚点，通过锚点加载动态链接库的类，接着创建出这个类的对象，然后调用其中的方法
install(TARGETS test_plugin
    DESTINATION lib/${PROJECT_NAME}
)

ament_package()
