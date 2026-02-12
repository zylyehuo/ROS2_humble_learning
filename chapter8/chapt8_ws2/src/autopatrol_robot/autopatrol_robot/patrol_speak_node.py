import rclpy
from geometry_msgs.msg import PoseStamped, Pose
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult
from tf2_ros import TransformListener, Buffer
from tf_transformations import euler_from_quaternion, quaternion_from_euler
import math  # 角度转弧度函数
from rclpy.duration import Duration
from autopatrol_interfaces.srv import SpeechText # 添加自定义的消息接口

class PatrolNode(BasicNavigator):
    def __init__(self, node_name='patrol_node'):
        super().__init__(node_name)
        # 声明相关参数
        self.declare_parameter('initial_point', [0.0, 0.0, 0.0])  # [x, y, yaw(弧度)]
        self.declare_parameter('target_points', [0.0, 0.0, 0.0, 2.0, -1.0, 1.57])
        self.buffer = Buffer()
        self.listener = TransformListener(self.buffer, self)
        
        # 获取参数的值
        self.initial_point_ = self.get_parameter('initial_point').value
        self.target_points_ = self.get_parameter('target_points').value
        
        # 创建语音合成客户端
        self.speech_client_ = self.create_client(SpeechText, 'speech_text')

    def get_pose_by_xyyaw(self, x, y, yaw):
        """
          传入 x,y,yaw
          return: PoseStamped 对象
        """
        pose = PoseStamped()
        pose.header.frame_id = 'map'
        pose.pose.position.x = x
        pose.pose.position.y = y
        
        rotation_quat = quaternion_from_euler(0, 0, yaw)  # 从欧拉角转换为四元数，返回顺序是 [x, y, z, w]
        pose.pose.orientation.x = rotation_quat[0]
        pose.pose.orientation.y = rotation_quat[1]
        pose.pose.orientation.z = rotation_quat[2]
        pose.pose.orientation.w = rotation_quat[3]
        
        return pose

    def init_robot_pose(self):
        """
          初始化机器人的位姿
        """
        # 从参数获取初始化点
        self.initial_point_ = self.get_parameter('initial_point').value
        
        # 合成位姿并进行初始化
        initial_pose = self.get_pose_by_xyyaw(self.initial_point_[0], self.initial_point_[1], self.initial_point_[2])
        self.setInitialPose(initial_pose)
        
        # 等待导航可用
        self.waitUntilNav2Active()

    def get_target_points(self):
        """
          通过参数值获取目标点集合        
        """
        points = []
        self.target_points_ = self.get_parameter('target_points').value
        
        for index in range(int(len(self.target_points_)/3)):
            x = self.target_points_[index*3]
            y = self.target_points_[index*3+1]
            yaw = self.target_points_[index*3+2]
            points.append([x, y, yaw])
            
            self.get_logger().info(f'获取到目标点: {index}->({x},{y},{yaw})')
            
        return points

    def nav_to_pose(self, target_point):
        """
          导航到目标点
        """
        self.waitUntilNav2Active()  # 等待导航可用
        
        result = self.goToPose(target_point)
        
        while not self.isTaskComplete():
            feedback = self.getFeedback()
            if feedback:
                self.get_logger().info(f'剩余距离: {feedback.distance_remaining} 米')
                self.get_logger().info(f'预计: {Duration.from_msg(feedback.estimated_time_remaining).nanoseconds / 1e9} s 后到达')
                
        # 最终结果判断
        result = self.getResult()
        self.get_logger().info(f'导航 result: {result}')
        
        if result == TaskResult.SUCCEEDED:
            self.get_logger().info('导航结果：成功')
        elif result == TaskResult.CANCELED:
            self.get_logger().warn('导航结果：被取消')
        elif result == TaskResult.FAILED:
            self.get_logger().error('导航结果：失败')
        else:
            self.get_logger().error('导航结果：返回状态无效')

    def get_current_pose(self):
        """
          通过 TF 获取机器人当前的位姿
        """
        while rclpy.ok():
            try:
                tf = self.buffer_.lookup_transform('map', 'base_footprint', rclpy.time.Time(seconds=0), rclpy.time.Duration(seconds=1))
                transform = tf.transform
                
                rotation_euler = euler_from_quaternion([
                    transform.rotation.x,
                    transform.rotation.y,
                    transform.rotation.z,
                    transform.rotation.w
                ])
                
                self.get_logger().info(f'平移:{transform.translation}')
                self.get_logger().info(f'旋转四元数:{transform.rotation}')
                self.get_logger().info(f'旋转欧拉角:{rotation_euler}')
                
                return transform
            except Exception as e:
                self.get_logger().warn(f'获取坐标变换失败，原因: {str(e)}')
    
    def speech_text(self, text):
        """
          调用服务合成语音
        """
        while not self.speech_client_.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('语音合成服务未上线，等待中...')

        request = SpeechText.Request()
        request.text = text
        
        future = self.speech_client_.call_async(request)  # 异步调用服务，发送请求
        
        rclpy.spin_until_future_complete(self, future)  # 等待服务端处理完成
        
        if future.result() is not None:
            result = future.result().result
            if result:
                self.get_logger().info(f'语音合成成功：{text}')
            else:
                self.get_logger().warn(f'语音合成失败：{text}')
        else:
            self.get_logger().warn('语音合成服务响应失败')
            
def main():
    rclpy.init()
    patrol = PatrolNode()  # 节点
    # rclpy.spin(patrol)  # 生成参数时候临时使用
    patrol.speech_text(text='正在准备初始化位置')
    patrol.init_robot_pose()  # 初始化机器人的位姿 
    patrol.speech_text(text='位置初始化完成')
    
    while rclpy.ok():
        points = patrol.get_target_points()
        for point in points:
            x, y, yaw = point[0], point[1], point[2]
            target_pose = patrol.get_pose_by_xyyaw(x, y, yaw)
            patrol.speech_text(text=f'正在准备前往目标点{x},{y}')
            patrol.nav_to_pose(target_pose)
            
    rclpy.shutdown()

if __name__ == '__main__':
    main()
    