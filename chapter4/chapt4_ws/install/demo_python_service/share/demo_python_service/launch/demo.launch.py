import launch
import launch_ros

def generate_launch_description():
    """
    产生 launch 描述
    """
    action_node_turtlesim_node = launch_ros.actions.Node(
        package='turtlesim',  # 功能包名字
        executable='turtlesim_node',  # 可执行文件名字
        output = 'screen',  # 日志输出位置
    )
    
    action_node_patrol_client_set_other = launch_ros.actions.Node(
        package='demo_cpp_service',
        executable='patrol_client_set_other',
        output = 'log',
    )
    
    action_node_turtle_control_param_callback = launch_ros.actions.Node(
        package='demo_cpp_service',
        executable='turtle_control_param_callback',
        output = 'both',
    )
    
    return launch.LaunchDescription([
        # actions 动作
        action_node_turtlesim_node,
        action_node_patrol_client_set_other,
        action_node_turtle_control_param_callback,
    ])