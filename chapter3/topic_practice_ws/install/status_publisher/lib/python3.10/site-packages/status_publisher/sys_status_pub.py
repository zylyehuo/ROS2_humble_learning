import rclpy
from status_interfaces.msg import SystemStatus
from rclpy.node import Node
import psutil
import platform

class SysStatusPub(Node):
    def __init__(self, node_name):
        super().__init__(node_name)
        # self.create_publisher(消息接口， 话题名字， QoS)
        self._status_publisher = self.create_publisher(
            SystemStatus, 'sys_status', 10
        )

        self._timer = self.create_timer(1.0, self.timer_callback)

    def timer_callback(self):
        """
        builtin_interfaces/Time stamp  # 时间戳
        string host_name  # 主机名字
        float32 cpu_percent  # cpu使用率
        float32 memory_percent  # 内存使用率
        float32 memory_total  # 内存总大小
        float32 memory_available  # 剩余内存
        float64 net_sent  # 网络发送数据总量 1MB=8Mb
        float64 net_recv  # 网络数据接受总量 MB
        """
        cpu_percent = psutil.cpu_percent()  # CPU使用率
        memory_info = psutil.virtual_memory()  # 内存信息
        net_io_counters = psutil.net_io_counters()  # 网络相关的输入输出信息
        
        msg = SystemStatus()
        
        msg.stamp = self.get_clock().now().to_msg()  # 获取当前的时间
        msg.host_name = platform.node()  # 主机名字
        msg.cpu_percent = cpu_percent
        msg.memory_percent = memory_info.percent
        msg.memory_total = memory_info.total / 1024 / 1024  # b -> kb -> Mb
        msg.memory_available = memory_info.available / 1024 / 1024
        msg.net_sent = net_io_counters.bytes_sent / 1024 / 1024
        msg.net_recv = net_io_counters.bytes_recv / 1024 / 1024
        
        self.get_logger().info(f"发布: {str(msg)}")
        
        self._status_publisher.publish(msg)

def main():
    rclpy.init()
    node = SysStatusPub('sys_status_pub')
    rclpy.spin(node)
    rclpy.shutdown()
