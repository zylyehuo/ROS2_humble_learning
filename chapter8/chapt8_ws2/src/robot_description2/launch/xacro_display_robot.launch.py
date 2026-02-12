import launch
import launch_ros
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    # 获取默认的 xacro 路径
    xacro_package_path = get_package_share_directory("robot_description2")  # 传入功能包的名字
    xacro_file = os.path.join(xacro_package_path, "urdf", "robot", "robot.urdf.xacro")
    
    # 获取默认的 rviz 配置文件路径
    rviz_config_file = os.path.join(xacro_package_path, "config", "display_robot_model.rviz")
    
    # 声明一个 urdf 路径的参数，方便修改
    action_declare_urdf_file = launch.actions.DeclareLaunchArgument("xacro_file", default_value=xacro_file, description="加载的模型文件路径")
    
    # 通过文件路径获取内容，并转换成参数值对象，以供传入 robot_state_publisher
    # 使用 xacro 命令，将 xacro 文件解析为 urdf 文件
    substitutions_command_result = launch.substitutions.Command(['xacro ', launch.substitutions.LaunchConfiguration("xacro_file")])
    robot_description_value = launch_ros.parameter_descriptions.ParameterValue(substitutions_command_result, value_type=str)
    
    action_robot_state_publisher = launch_ros.actions.Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[{"robot_description": robot_description_value}],
    )

    action_joint_state_publisher = launch_ros.actions.Node(
        package="joint_state_publisher",
        executable="joint_state_publisher",
    )
    
    action_rviz_node = launch_ros.actions.Node(
        package="rviz2",
        executable="rviz2",
        arguments=["-d", rviz_config_file],
    )
    
    return launch.LaunchDescription([
        action_declare_urdf_file,
        action_robot_state_publisher,
        action_joint_state_publisher,
        action_rviz_node,
    ])
    