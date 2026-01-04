import rclpy
from rclpy.node import Node
from chapt4_interfaces.srv import FaceDetector
import face_recognition
import cv2
from ament_index_python.packages import get_package_share_directory  # 获取功能包share目录绝对路径
import os
from cv_bridge import CvBridge
import time

class FaceDetectNode(Node):
    def __init__(self, node_name):
        super().__init__(node_name)
        self.face_detect_srv = self.create_service(FaceDetector, 'face_detect', self.detect_face_callback)
        self._bridge = CvBridge()
        self._number_of_times_to_upsample = 1
        self._model='hog'
        self._package_path = get_package_share_directory('demo_python_service')
        self._default_image_path = os.path.join(self._package_path, "resource", "default.jpg")
        self.get_logger().info(f"人脸检测服务已经启动")
        
    def detect_face_callback(self,  request, response):
        if request.image.data:
            cv_image = self._bridge.imgmsg_to_cv2(request.image)
        else:
            cv_image = cv2.imread(self._default_image_path)
            self.get_logger().info(f"传入图像为空，使用默认图像")

        # cv_image 此时已经是一个 OpenCV 格式的图像了
        start_time = time.time()
        
        self.get_logger().info(f"加载图像完成，开始识别")
        
        # 使用 face_recognition 在图片中查找人脸
        face_locations_res = face_recognition.face_locations(cv_image, number_of_times_to_upsample=self._number_of_times_to_upsample, model=self._model)  # 参数(图片，上采样次数，识别人脸的模型)  上采样次数：越高的次数可以找到越小的脸
        
        # 记录下使用时间
        response.use_time = time.time() - start_time
        
        # 识别到的人脸数量
        response.number = len(face_locations_res)
        
        # 在图片中绘制检测到人脸的边框
        for top, right, bottom, left in face_locations_res:
            response.top.append(top)
            response.right.append(right)
            response.bottom.append(bottom)
            response.left.append(left)
            
        return response  # 必须返回 response
    
def main():
    rclpy.init()
    node = FaceDetectNode('face_detect_node')
    rclpy.spin(node)
    rclpy.shutdown()
