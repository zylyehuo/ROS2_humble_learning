import rclpy
from rclpy.node import Node

class PersonNode(Node):
    def __init__(self, node_name: str, name: str, age: int) -> None:
        super().__init__(node_name)
        print("PersonNode __init__ 方法被调用了")
        self.name = name
        self.age = age
    
    def eat(self, food: str):
        """
        Docstring for eat
        
        :param self: Description
        :param food: 食物名称
        :type food: str
        """
        # print(f"{self.name}, {self.age}岁，爱吃{food}")
        self.get_logger().info(f"{self.name}, {self.age}岁，爱吃{food}")
        
def main():
    rclpy.init()
    node = PersonNode("person_node", "法外狂徒张三", 18)
    node.eat("鱼香肉丝")
    rclpy.spin(node)
    rclpy.shutdown()