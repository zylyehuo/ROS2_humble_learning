from geometry_msgs.msg import PoseStamped
# nav2_simple_commander 负责将 PoseStamped 格式转化为 geometry_msgs/msg/PoseWithCovarianceStamped
from nav2_simple_commander.robot_navigator import BasicNavigator
import rclpy


def main():
    rclpy.init()
    nav = BasicNavigator()  # 是一个节点
    initial_pose = PoseStamped()
    initial_pose.header.frame_id = 'map'
    initial_pose.header.stamp = nav.get_clock().now().to_msg()
    initial_pose.pose.position.x = 0.0
    initial_pose.pose.position.y = 0.0
    initial_pose.pose.orientation.w = 1.0  # 表示朝向是 0
    nav.setInitialPose(initial_pose)
    nav.waitUntilNav2Active()  # 等待导航可用
    rclpy.spin(nav)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
