#include <rclcpp/rclcpp.hpp>
#include <geometry_msgs/msg/twist.hpp>
#include <chrono>
#include <turtlesim/msg/pose.hpp>

using namespace std::chrono_literals;

class TurtleControlNode : public rclcpp::Node
{
private:
    rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr _publisher; // 发布者的智能指针
    rclcpp::Subscription<turtlesim::msg::Pose>::SharedPtr _subscriber;  // 订阅者的智能指针
    double _target_x{1.0};
    double _target_y{1.0};
    double _k{1.0};  // 比例系数
    double _max_speed{3.0};  // 最大速度

public:
    explicit TurtleControlNode(const std::string &node_name) : Node(node_name) // explicit 防止隐式构造对象，提高代码可维护性
    {
        _publisher = this->create_publisher<geometry_msgs::msg::Twist>("/turtle1/cmd_vel", 10);
        _subscriber = this->create_subscription<turtlesim::msg::Pose>("/turtle1/pose", 10, std::bind(&TurtleControlNode::on_pose_received_callback, this, std::placeholders::_1));
    }

    void on_pose_received_callback(const turtlesim::msg::Pose::SharedPtr pose) // 参数：收到数据的共享指针
    {
        // 获取当前位置和朝向(角度)
        auto current_x = pose->x;
        auto current_y = pose->y;
        RCLCPP_INFO(get_logger(), "当前: x=%f, y=%f", current_x, current_y);

        auto current_theta = pose->theta;
        RCLCPP_INFO(get_logger(), "当前: theta=%f", current_theta);

        // 计算当前位置和目标位置的距离差和角度差
        auto distance = std::sqrt(
            (_target_x - current_x)*(_target_x - current_x)+
            (_target_y - current_y)*(_target_y - current_y)
        );
        
        auto angle = std::atan2((_target_y - current_y), (_target_x - current_x)) - current_theta;

        // 编写控制策略
        auto msg = geometry_msgs::msg::Twist();

        if(distance > 0.1)
        {
            if(fabs(angle) > 0.2)
            {
                msg.angular.z = fabs(angle);
            }
            else
            {
                msg.linear.x = _k * distance;
            }
        }

        // 限制最大速度
        if(msg.linear.x > _max_speed)
        {
            msg.linear.x = _max_speed;
        }

        // 发布消息
        _publisher->publish(msg);
    }
};

int main(int argc, char *argv[])
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<TurtleControlNode>("turtle_control");
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}