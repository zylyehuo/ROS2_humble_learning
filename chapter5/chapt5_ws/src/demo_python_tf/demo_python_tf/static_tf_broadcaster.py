import rclpy
from rclpy.node import Node
from tf2_ros import StaticTransformBroadcaster  # 静态坐标发布器
from geometry_msgs.msg import TransformStamped  # 消息接口
from tf_transformations import quaternion_from_euler  # 欧拉角转四元数
import math  # 角度转弧度

"""
pip3 install --upgrade transforms3d
"""
"""
ros2 topic list

ros2 topic echo /tf_static

ros2 topic info /tf_static -v

ros2 run tf2_ros tf2_echo base_link camera_link
"""

class StaticTFBroadcaster(Node):
    def __init__(self, node_name):
        super().__init__(node_name)
        self._static_broadcaster = StaticTransformBroadcaster(self)  # self 就是节点本身
        self.publish_static_tf()

    def publish_static_tf(self):  # 发布静态坐标: 从 base_link 到 camera_link
        transform = TransformStamped()
        transform.header.stamp = self.get_clock().now().to_msg()  # 时间戳
        transform.header.frame_id = "base_link"  # 父节点坐标系
        transform.child_frame_id = "camera_link"  # 子节点坐标系
        
        transform.transform.translation.x = 0.5
        transform.transform.translation.y = 0.3
        transform.transform.translation.z = 0.6
        
        """
            math.radians() 角度转弧度
            quaternion_from_euler 欧拉角转四元数 顺序为：[x, y, z, w]
        """
        q = quaternion_from_euler(math.radians(180), 0, 0)
        
        # 旋转部分进行赋值
        transform.transform.rotation.x = q[0]
        transform.transform.rotation.y = q[1]
        transform.transform.rotation.z = q[2]
        transform.transform.rotation.w = q[3]
        
        # 发布静态坐标关系
        self._static_broadcaster.sendTransform(transform)
        self.get_logger().info(f"发布静态TF：{transform}")
        
def main():
    rclpy.init()
    node = StaticTFBroadcaster("static_tf_broadcaster")
    rclpy.spin(node)
    rclpy.shutdown()
