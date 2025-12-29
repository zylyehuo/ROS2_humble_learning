import rclpy
from rclpy.node import Node
import requests
from example_interfaces.msg import String
from queue import Queue

"""
zylyehuo@LAPTOP-4FQQUA1G:~/ROS2_learning/chapter3$ python3 -m http.server
"""

class NovelPubNode(Node):
    def __init__(self, node_name):
        super().__init__(node_name)
        self.get_logger().info(f"{node_name}, 启动")
        # 创建队列 Queue()
        self._novel_queue = Queue()
        # 创建发布者 self.create_publisher(消息接口, 话题名字，服务质量配置)
        self._novel_publisher = self.create_publisher(String, "novel", 10)
        # 创建定时器 self.create_timer(时间周期(秒)，回调函数)
        self.create_timer(5, self.timer_callback)
        
    def timer_callback(self):
        if self._novel_queue.qsize() > 0:
            line = self._novel_queue.get()
            # 按照消息接口的类型构建“消息”
            msg = String()
            msg.data = line
            self._novel_publisher.publish(msg)
            self.get_logger().info(f"发布了：{msg},")
            
    def download(self, url):
        response = requests.get(url)
        response.encoding = 'utf-8'
        text = response.text  # 下载小说内容
        self.get_logger().info(f"下载 {url}, {len(text)}")
        # 按行分割小说内容，并按行加入队列
        for line in text.splitlines():
            self._novel_queue.put(line)
         
def main():
    rclpy.init()
    node = NovelPubNode("novel_pub")
    node.download("http://localhost:8000/novel1.txt")
    rclpy.spin(node)
    rclpy.shutdown()
