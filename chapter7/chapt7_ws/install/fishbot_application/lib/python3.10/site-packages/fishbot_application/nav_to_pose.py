from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult
import rclpy
from rclpy.duration import Duration


def main():
    rclpy.init()
    navigator = BasicNavigator()  # 节点
    navigator.waitUntilNav2Active()  # 等待导航可用
    
    goal_pose = PoseStamped()  # 设置目标点
    goal_pose.header.frame_id = 'map'
    goal_pose.header.stamp = navigator.get_clock().now().to_msg()
    goal_pose.pose.position.x = 0.0
    goal_pose.pose.position.y = 0.0
    goal_pose.pose.orientation.w = 1.0
    
    navigator.goToPose(goal_pose)  # 向 action 服务发送目标点
    
    while not navigator.isTaskComplete():
        feedback = navigator.getFeedback()  # 获取反馈
        navigator.get_logger().info(f'剩余距离: {feedback.distance_remaining} 米')
        navigator.get_logger().info(f'预计: {Duration.from_msg(feedback.estimated_time_remaining).nanoseconds / 1e9} s 后到达')
        
        # 超时自动取消
        if Duration.from_msg(feedback.navigation_time) > Duration(seconds=600.0):
            navigator.cancelTask()
            
    result = navigator.getResult()  # 获取导航结果
    navigator.get_logger().info(f'导航 result: {result}')
    
    if result == TaskResult.SUCCEEDED:
        navigator.get_logger().info('导航结果：成功')
    elif result == TaskResult.CANCELED:
        navigator.get_logger().warn('导航结果：被取消')
    elif result == TaskResult.FAILED:
        navigator.get_logger().error('导航结果：失败')
    else:
        navigator.get_logger().error('导航结果：返回状态无效')

if __name__ == '__main__':
    main()