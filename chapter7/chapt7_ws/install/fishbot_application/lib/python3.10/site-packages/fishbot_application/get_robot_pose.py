import rclpy
from rclpy.node import Node
from tf2_ros import TransformListener, Buffer  # 坐标监听者
from tf_transformations import euler_from_quaternion  # 四元数转欧拉角


class TFListener(Node):

    def __init__(self):
        super().__init__('tf2_listener')
        self.buffer = Buffer()
        self.listener = TransformListener(self.buffer, self)
        self.timer = self.create_timer(1, self.get_transform)

    def get_transform(self):
        if self.buffer.can_transform('map', 'base_footprint', rclpy.time.Time(), rclpy.time.Duration(seconds=1)):
            try:
                tf = self.buffer.lookup_transform('map', 'base_footprint', rclpy.time.Time())
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
            except Exception as e:
                self.get_logger().warn(f'获取坐标变换失败，原因: {str(e)}')
        else:
            self.get_logger().info('等待 map 到 base_footprint 的坐标变换中...')


def main():
    rclpy.init()
    node = TFListener()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()