import rclpy
from rclpy.node import Node
from autopatrol_interfaces.srv import SpeechText
import espeakng  # 语音合成的库

class Speaker(Node):
    def __init__(self, node_name):
        super().__init__(node_name)
        self.speech_service = self.create_service(SpeechText, 'speech_text', self.speak_text_callback)
        self.speaker = espeakng.Speaker()
        self.speaker.voice = 'zh'

    def speak_text_callback(self, request, response):
        self.get_logger().info('正在准备朗读 %s' % request.text)
        self.speaker.say(request.text)
        self.speaker.wait()
        response.result = True
        return response


def main(args=None):
    rclpy.init()
    node = Speaker('speaker')
    rclpy.spin(node)
    rclpy.shutdown()
