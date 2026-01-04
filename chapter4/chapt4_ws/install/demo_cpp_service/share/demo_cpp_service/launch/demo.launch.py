import launch
import launch_ros

def generate_launch_description():
    # 声明一个 launch 参数，在命令行使用
    # ros2 launch demo_cpp_service demo.launch.py launch_arg_bg:=150
    action_declare_arg_background_g = launch.actions.DeclareLaunchArgument("launch_arg_bg", default_value="150")
    """
    产生 launch 描述
    """
    action_node_turtlesim_node = launch_ros.actions.Node(
        package='turtlesim',  # 功能包名字
        executable='turtlesim_node',  # 可执行文件名字
        # 将 launch 文件的参数“替换”为节点可以用的参数
        # parameters=[{要启动的节点的参数名字:launch文件中定义的参数值}],
        parameters=[{"background_g":launch.substitutions.LaunchConfiguration("launch_arg_bg", default="150")}],
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
        # actions “动作”
        action_declare_arg_background_g,
        action_node_turtlesim_node,
        action_node_patrol_client_set_other,
        action_node_turtle_control_param_callback,
    ])