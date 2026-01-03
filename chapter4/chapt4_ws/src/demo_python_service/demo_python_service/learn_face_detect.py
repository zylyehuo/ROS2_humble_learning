import face_recognition
import cv2
from ament_index_python.packages import get_package_share_directory  # 获取功能包share目录绝对路径

def main():
    # 获取图片的真实路径
    package_share_directory = get_package_share_directory('demo_python_service')  # 参数就是功能包的名字
    default_image_path = package_share_directory + "/resource/default.jpg"
    print(f"图片的绝对路径：{default_image_path}")

    # 使用 OpenCV 加载图片
    image = cv2.imread(default_image_path)

    # 使用 face_recognition 在图片中查找人脸
    face_locations_res = face_recognition.face_locations(image, number_of_times_to_upsample=1, model='hog')  # 参数(图片，上采样次数，识别人脸的模型)  上采样次数：越高的次数可以找到越小的脸
    
    # 在图片中绘制检测到人脸的边框
    for top, right, bottom, left in face_locations_res:
        cv2.rectangle(image, (left, top), (right, bottom), (255, 0, 0), 4)
        
    # 结果显示
    cv2.imshow("Face Detect Result", image)
    cv2.waitKey(0)
