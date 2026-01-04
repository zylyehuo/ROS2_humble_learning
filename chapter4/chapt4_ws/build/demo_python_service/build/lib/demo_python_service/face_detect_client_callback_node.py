import rclpy
from rclpy.node import Node
from chapt4_interfaces.srv import FaceDetector
import face_recognition
import cv2
from ament_index_python.packages import get_package_share_directory  # 获取功能包share目录绝对路径
import os
from cv_bridge import CvBridge
import time
from rcl_interfaces.msg import Parameter, ParameterValue, ParameterType
from rcl_interfaces.srv import SetParameters

class FaceDetectClientNode(Node):
    def __init__(self, node_name):
        super().__init__(node_name)
        self._face_detect_cli = self.create_client(FaceDetector, 'face_detect')  # 创建客户端 create_client(服务类型, 服务名字)
        self._bridge = CvBridge()
        self._package_path = get_package_share_directory('demo_python_service')
        self._default_image_path = os.path.join(self._package_path, "resource", "test1.jpg")
        self._image = cv2.imread(self._default_image_path)
        self.get_logger().info(f"人脸检测客户端已经启动")
    
    def call_set_parameters(self, parameters):
        """
        调用服务，修改参数值
        """
        # 创建一个客户端，等待服务上线
        update_param_client  = self.create_client(SetParameters, "/face_detect_param_callback_node/set_parameters")
        while update_param_client.wait_for_service(timeout_sec=1.0) == False:
            self.get_logger().info(f"等待参数更新以及服务端上线")
            
        # 创建 request
        request  = SetParameters.Request()
        request.parameters = parameters
        
        # 调用服务端更新参数
        future = update_param_client.call_async(request)
        rclpy.spin_until_future_complete(self, future)
        response = future.result()
        
        return response
    
    def update_detect_model(self, model='hog'):
        """
        根据传入的 model，构造 parameters，然后调用 call_set_parameters 更新服务端的参数
        """
        # 创建参数对象
        param = Parameter()
        param.name = '_model'
        
        # 赋值，创建 param_value
        param_value = ParameterValue()
        param_value.string_value = model
        param_value.type = ParameterType.PARAMETER_STRING
        param.value = param_value
        
        # 请求更新参数
        response = self.call_set_parameters([param])
        for result in response.results:
            if result.successful:
                self.get_logger().info(f"设置参数结果：{result.successful}，{param.value.string_value}，原因：{result.reason}")
        
    def send_request(self):
        # 判断服务端是否在线
        while self._face_detect_cli.wait_for_service(timeout_sec=1.0) == False:
            self.get_logger().info(f"等待服务端上线")

        # 构造 request
        request = FaceDetector.Request()
        request.image = self._bridge.cv2_to_imgmsg(self._image)
        
        # 发送请求，异步获取结果，并等待处理完成
        future = self._face_detect_cli.call_async(request)  # 现在的 future 里面并没有包含响应结果，需要等待服务端处理完成，才会把结果放到 future 中
        
        # while not future.done():
        #     time.sleep(1.0)  # 休眠当前进程，等待服务完成，造成当前进程无法再接收来自服务端的返回，导致永远没有办法完成【future.done() 返回 True】
        
        # =========================================================异步的实现方法=========================================================
        # rclpy.spin_until_future_complete(self, future)  # 等待服务端返回响应
        
        # # 获取任务执行结果（获取响应）
        # response = future.result()
        # self.get_logger().info(f"接收到响应，共检测到{response.number}张人脸，耗时:{response.use_time}秒")
        
        # self.show_response(response)
        # ================================================================================================================================
        
        # =======================================================回调函数的实现方法=========================================================        
        future.add_done_callback(self.result_callback)
        # ================================================================================================================================
        
    def result_callback(self, result_future):
        # 获取任务执行结果（获取响应）
        response = result_future.result()
        self.get_logger().info(f"接收到响应，共检测到{response.number}张人脸，耗时:{response.use_time}秒")
        # self.show_response(response)
            
    def show_response(self, response):
        for ind in range(response.number):
            top = response.top[ind]
            right = response.right[ind]
            bottom = response.bottom[ind]
            left = response.left[ind]
            
            # 在图片中绘制检测到人脸的边框
            cv2.rectangle(self._image, (left, top), (right, bottom), (255, 0, 0), 4)

        # 结果显示
        cv2.imshow("Face Detect Result", self._image)
        cv2.waitKey(0)  # 也会导致阻塞，会导致 spin 无法正常运行
    
def main():
    rclpy.init()
    node = FaceDetectClientNode('face_detect_client_node')
    node.update_detect_model('hog')
    node.send_request()
    node.update_detect_model('cnn')
    node.send_request()
    rclpy.spin(node)
    rclpy.shutdown()
