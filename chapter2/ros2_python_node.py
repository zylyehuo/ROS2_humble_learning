import rclpy

from rclpy.node import Node

def main():
    rclpy.init()  # 初始化工作，分配资源
    node = Node("python_node")  # 创建节点，并取一个名字
    
    node.get_logger().info("hello python_node")  # 获取日志管理模块，info()进行信息提示
    
    rclpy.spin(node)  # 运行节点，只要没有打断或者主动退出，就会一直阻塞在这
    rclpy.shutdown()  # 主动退出时，进行清理
    
if __name__ == "__main__":
    main()
