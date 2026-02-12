import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/zylyehuo/ROS2_learning/chapter8/chapt8_ws2/install/autopatrol_robot'
