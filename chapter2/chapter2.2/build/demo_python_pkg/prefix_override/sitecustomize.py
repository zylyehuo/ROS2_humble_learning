import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/zylyehuo/ROS2_learning/chapter2/chapter2.2/install/demo_python_pkg'
