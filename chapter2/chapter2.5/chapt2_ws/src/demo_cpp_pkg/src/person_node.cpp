#include "rclcpp/rclcpp.hpp"

class PersonNode : public rclcpp::Node
{
private:
    std::string _name;
    int _age;

public:
    PersonNode(const std::string &node_name, const std::string &name, const int &age)
        : Node(node_name) /* 调用父类的构造函数，等同于 python 中的 super().__init__(node_name) */
    {
        this->_name = name;
        (*this)._age = age;
    };

    void eat(const std::string &food)
    {
        RCLCPP_INFO(this->get_logger(), "我是%s, %d岁, 爱吃%s", this->_name.c_str(), this->_age, food.c_str());
    };
};

int main(int argc, char** argv)  // 设置入口参数
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<PersonNode>("person_node", "法外狂徒张三", 18);
    RCLCPP_INFO(node->get_logger(), "hello person_node");
    node->eat("meat");
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}
