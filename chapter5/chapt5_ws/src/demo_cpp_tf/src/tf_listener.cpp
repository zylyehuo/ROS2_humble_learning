#include "rclcpp/rclcpp.hpp"
#include "geometry_msgs/msg/transform_stamped.hpp"  // 提供消息接口
#include "tf2/LinearMath/Quaternion.hpp"  // 提供 tf2::Quaternion 类
#include "tf2_geometry_msgs/tf2_geometry_msgs.hpp"  // 消息类型转换函数
#include "tf2_ros/transform_listener.hpp"  // 坐标监听器
#include "tf2_ros/buffer.hpp"
#include "tf2/utils.hpp"  // 四元数转欧拉角
#include "chrono"

using namespace std::chrono_literals;  // s ms

/*
ros2 topic list

ros2 topic echo /tf

ros2 topic info /tf -v

ros2 run tf2_ros tf2_echo base_link target_point
*/

class TFListener: public rclcpp::Node
{
private:
    std::shared_ptr<tf2_ros::TransformListener> _listener;
    rclcpp::TimerBase::SharedPtr _timer;  // 定时器
    std::shared_ptr<tf2_ros::Buffer> _buffer;  // 将监听到的坐标关系存储下来

public:
    TFListener(std::string node_name): Node(node_name)
    {
        _buffer = std::make_shared<tf2_ros::Buffer>(this->get_clock());
        _listener = std::make_shared<tf2_ros::TransformListener>(*_buffer, this);
        // 把成员函数当做回调函数，使用函数包装器 std::bind(&类::成员函数, 对象指针)
        _timer = this->create_wall_timer(1s, std::bind(&TFListener::getTransform, this));
    }

    void getTransform()
    {
        // 到 _buffer 里查询坐标关系
        try
        {
            // 查询从 target_point 到 base_link 的坐标关系
            const auto transform = _buffer->lookupTransform("base_link", "target_point", this->get_clock()->now(), rclcpp::Duration::from_seconds(1.0f));
        
            // 获取查询结果
            auto _translation = transform.transform.translation;
            auto _rotation = transform.transform.rotation;

            //  四元数转欧拉角
            double y, p, r;
            tf2::getEulerYPR(_rotation, y, p, r);
            RCLCPP_INFO(this->get_logger(), "平移：%f, %f, %f", _translation.x, _translation.y, _translation.z);
            RCLCPP_INFO(this->get_logger(), "旋转[欧拉角]：%f, %f, %f", y, p, r);

        }
        catch(const std::exception& e)
        {
            // 没有查询到坐标关系
            RCLCPP_WARN(this->get_logger(), "%s", e.what());
        }
        
    }

};

int main(int argc, char* argv[])
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<TFListener>("tf_listener");
    rclcpp::spin(node);
    rclcpp::shutdown();

    return 0;
}