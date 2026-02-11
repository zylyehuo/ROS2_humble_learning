import os
import launch
import launch_ros
from ament_index_python.packages import get_package_share_directory  # 获取功能包的 share 目录
from launch.launch_description_sources import PythonLaunchDescriptionSource


def generate_launch_description():
    # 获取与拼接默认路径
    autopatrol_robot_dir = get_package_share_directory('autopatrol_robot')
    patrol_config_path = os.path.join(autopatrol_robot_dir, 'config', 'patrol_config.yaml')
    
    # 动作一
    action_patrol_speak_node = launch_ros.actions.Node(
        package='autopatrol_robot',  # 功能包名字
        executable='patrol_speak_image_node',  # 可执行文件名字
        output='screen',
        parameters=[patrol_config_path]  # 参数
    )
    
    # 动作二
    action_speaker = launch_ros.actions.Node(
        package='autopatrol_robot',
        executable='speaker',
        output='screen',
    )

    return launch.LaunchDescription([
        action_patrol_speak_node,
        action_speaker,
    ])