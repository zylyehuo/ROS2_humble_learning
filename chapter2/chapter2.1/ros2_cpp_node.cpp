#include "rclcpp/rclcpp.hpp"

int main(int argc, char** argv)  // 设置入口参数
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<rclcpp::Node>("cpp_node");
    RCLCPP_INFO(node->get_logger(), "hello cpp_node");
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}