import espeakng
import rclpy
from rclpy.node import Node
from example_interfaces.msg import String
from queue import Queue
import threading
import time

class NovelSubNode(Node):
    def __init__(self, node_name):
        super().__init__(node_name)
        self.get_logger().info(f"{node_name}, 启动")
        self._novel_queue = Queue()
        self._novel_subscriber = self.create_subscription(String, 'novel', self.novel_callback, 10)
        self._speak_thread = threading.Thread(target=self.speak_thread_func)
        self._speak_thread.start()  # python 当中的线程要自己启动一下
        
    def novel_callback(self, msg):
        self._novel_queue.put(msg.data)

    def speak_thread_func(self):
        speaker = espeakng.Speaker()
        speaker.voice = 'zh'  # 设置语音为中文
        
        while rclpy.ok():  # 检测当前ROS上下文是否正常
            if self._novel_queue.qsize() > 0:
                text = self._novel_queue.get()
                self.get_logger().info(f"朗读：{text}")
                speaker.say(text)  # 开始说
                speaker.wait()  # 等待说完
            else:
                # 让当前的线程休眠 1s
                time.sleep(1)
            
def main():
    rclpy.init()
    node = NovelSubNode("novel_sub")
    rclpy.spin(node)
    rclpy.shutdown()
