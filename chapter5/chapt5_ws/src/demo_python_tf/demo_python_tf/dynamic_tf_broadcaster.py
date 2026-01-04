import rclpy
from rclpy.node import Node
from tf2_ros import TransformBroadcaster  # 动态坐标发布器
from geometry_msgs.msg import TransformStamped  # 消息接口
from tf_transformations import quaternion_from_euler  # 欧拉角转四元数
import math  # 角度转弧度

"""
pip3 install --upgrade transforms3d
"""
"""
ros2 topic list

ros2 topic echo /tf

ros2 topic info /tf -v

ros2 run tf2_ros tf2_echo camera_link bottle_link
"""

class DynamicTFBroadcaster(Node):
    def __init__(self, node_name):
        super().__init__(node_name)
        self._broadcaster = TransformBroadcaster(self)  # self 就是节点本身
        self._timer =  self.create_timer(0.01, self.publish_dynamic_tf)  # 0.01秒 100赫兹 一秒钟发布100次tf

    def publish_dynamic_tf(self):  # 发布动态坐标: 从 camera_link 到 bottle_link
        transform = TransformStamped()
        transform.header.stamp = self.get_clock().now().to_msg()  # 时间戳
        transform.header.frame_id = "camera_link"  # 父节点坐标系
        transform.child_frame_id = "bottle_link"  # 子节点坐标系
        
        transform.transform.translation.x = 0.2
        transform.transform.translation.y = 0.3
        transform.transform.translation.z = 0.5
        
        """
        quaternion_from_euler 欧拉角转四元数 顺序为：[x, y, z, w]
        """
        q = quaternion_from_euler(0, 0, 0)
        
        # 旋转部分进行赋值
        transform.transform.rotation.x = q[0]
        transform.transform.rotation.y = q[1]
        transform.transform.rotation.z = q[2]
        transform.transform.rotation.w = q[3]
        
        # 发布静态坐标关系
        self._broadcaster.sendTransform(transform)
        self.get_logger().info(f"发布动态TF：{transform}")
        
def main():
    rclpy.init()
    node = DynamicTFBroadcaster("dynamic_tf_broadcaster")
    rclpy.spin(node)
    rclpy.shutdown()
