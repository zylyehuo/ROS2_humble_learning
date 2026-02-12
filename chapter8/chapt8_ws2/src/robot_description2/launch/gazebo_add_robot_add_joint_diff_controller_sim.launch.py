import launch
import launch_ros
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    # 获取默认的 xacro 路径
    # /home/zylyehuo/ROS2_learning/chapter6/chapt6_ws/src/robot_description2/urdf/robot/robot.urdf.xacro
    xacro_package_path = get_package_share_directory("robot_description2")  # 传入功能包的名字
    xacro_file = os.path.join(xacro_package_path, "urdf", "robot", "robot.urdf.xacro")
    
    # 获取默认的 gazebo 世界文件路径
    gazebo_world_file = os.path.join(xacro_package_path, "world", "custom_room.world")
    
    # 声明一个 urdf 路径的参数，方便修改
    action_declare_urdf_file = launch.actions.DeclareLaunchArgument("xacro_file", default_value=xacro_file, description="加载的模型文件路径")
    
    # 通过文件路径获取内容，并转换成参数值对象，以供传入 robot_state_publisher
    # 使用 xacro 命令，将 xacro 文件解析为 urdf 文件
    substitutions_command_result = launch.substitutions.Command(['xacro ', launch.substitutions.LaunchConfiguration("xacro_file")])
    robot_description_value = launch_ros.parameter_descriptions.ParameterValue(substitutions_command_result, value_type=str)
    
    # 静态 TF 的发布
    action_robot_state_publisher = launch_ros.actions.Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[{"robot_description": robot_description_value}],
    )

    # 每个关节的角度此时由 gazebo 直接发布
    # action_joint_state_publisher = launch_ros.actions.Node(
    #     package="joint_state_publisher",
    #     executable="joint_state_publisher",
    # )

    # 启动 gazebo 功能包自带的 launch 文件
    # ros2 launch gazebo_ros gazebo.launch.py world:=xxx.world
    action_gazebo_node = launch.actions.IncludeLaunchDescription(
        launch.launch_description_sources.PythonLaunchDescriptionSource(
            [get_package_share_directory("gazebo_ros"), "/launch", "/gazebo.launch.py"]
        ),
        launch_arguments=[("world", gazebo_world_file), ("verbose", "true")]
    )
    
    action_spawn_entity = launch_ros.actions.Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        # action_robot_state_publisher 中发布的话题：robot_description
        # 通过话题的方式加载 urdf 的内容
        # arguments=['-topic', 'urdf 的话题名字', '-entity', '机器人在 xacro 文件中的名字'],
        arguments=['-topic', '/robot_description', '-entity', 'second_robot'],
    )
    
    # 执行一个进程
    # 控制器的名字 “robot_joint_state_broadcaster” 要和 robot_ros2_controller.yaml 中的保持一致
    action_load_joint_state_controller = launch.actions.ExecuteProcess(
        cmd="ros2 control load_controller robot_joint_state_broadcaster --set-state active".split(" "),
        output="screen"
    )
    
    # 添加”力控“控制器
    # action_load_effort_controller = launch.actions.ExecuteProcess(
    #     cmd="ros2 control load_controller robot_effort_controller --set-state active".split(" "),
    #     output="screen"
    # )
    
    # 不要同时使用多个控制器一起控制轮子运动
    # 添加”差速“控制器
    action_load_diff_driver_controller = launch.actions.ExecuteProcess(
        cmd="ros2 control load_controller robot_diff_drive_controller --set-state active".split(" "),
        output="screen"
    )
    
    return launch.LaunchDescription([
        action_declare_urdf_file,
        action_robot_state_publisher,
        action_gazebo_node,
        action_spawn_entity,
        launch.actions.RegisterEventHandler(
            event_handler=launch.event_handlers.OnProcessExit(
                target_action=action_spawn_entity,
                on_exit=[action_load_joint_state_controller],  # 当上一个动作执行完成后再执行这个“控制器”动作
            )
        ),
        # launch.actions.RegisterEventHandler(
        #     event_handler=launch.event_handlers.OnProcessExit(
        #         target_action=action_load_joint_state_controller,
        #         on_exit=[action_load_effort_controller],
        #     )
        # ),
        launch.actions.RegisterEventHandler(
            event_handler=launch.event_handlers.OnProcessExit(
                target_action=action_load_joint_state_controller,
                on_exit=[action_load_diff_driver_controller],
            )
        ),
    ])
    