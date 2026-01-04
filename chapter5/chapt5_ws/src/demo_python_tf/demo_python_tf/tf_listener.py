import rclpy
from rclpy.node import Node
from tf2_ros import TransformListener, Buffer  # 坐标监听器、缓存器
from tf_transformations import euler_from_quaternion  # 四元数转欧拉角
import math  # 角度转弧度

class TFListener(Node):
    def __init__(self, node_name):
        super().__init__(node_name)
        self._buffer = Buffer()
        self._broadcaster = TransformListener(self._buffer, self)  # self 就是节点本身
        self._timer =  self.create_timer(1.0, self.get_tf)  # 1秒 一秒获取1次tf

    def get_tf(self):  # 实时查询坐标关系
        try:
            # lookup_transform("base_link", "bottle_link", 查询哪个时刻的【0代表最新】, 超过1秒查不到就不查了)
            result = self._buffer.lookup_transform("base_link", "bottle_link", rclpy.time.Time(seconds=0.0), rclpy.time.Duration(seconds=1.0))
            transform = result.transform
            self.get_logger().info(f"平移：{transform.translation}")
            self.get_logger().info(f"旋转：{transform.rotation}")
            rotation_euler = euler_from_quaternion([
                transform.rotation.x,
                transform.rotation.y,
                transform.rotation.z,
                transform.rotation.w,
            ])
            self.get_logger().info(f"旋转[欧拉角]：{rotation_euler}")
        except Exception as e:
            self.get_logger().warn(f"获取坐标变换失败，原因：{e}")
        
def main():
    rclpy.init()
    node = TFListener("tf_listener")
    rclpy.spin(node)
    rclpy.shutdown()
