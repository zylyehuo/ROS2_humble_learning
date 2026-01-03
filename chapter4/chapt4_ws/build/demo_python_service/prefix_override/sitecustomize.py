import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/zylyehuo/ROS2_learning/chapter4/chapt4_ws/install/demo_python_service'
