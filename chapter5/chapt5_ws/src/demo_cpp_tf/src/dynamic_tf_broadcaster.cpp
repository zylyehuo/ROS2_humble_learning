#include "rclcpp/rclcpp.hpp"
#include "geometry_msgs/msg/transform_stamped.hpp"  // 提供消息接口
#include "tf2/LinearMath/Quaternion.hpp"  // 提供 tf2::Quaternion 类
#include "tf2_geometry_msgs/tf2_geometry_msgs.hpp"  // 消息类型转换函数
#include "tf2_ros/transform_broadcaster.hpp"  // 动态坐标广播器
#include "chrono"

using namespace std::chrono_literals;  // s ms

/*
ros2 topic list

ros2 topic echo /tf

ros2 topic info /tf -v

ros2 run tf2_ros tf2_echo map base_link
*/

class TFBroadcaster: public rclcpp::Node
{
private:
    std::shared_ptr<tf2_ros::TransformBroadcaster> _broadcaster;
    rclcpp::TimerBase::SharedPtr _timer;  // 定时器

public:
    TFBroadcaster(std::string node_name): Node(node_name)
    {
        _broadcaster = std::make_shared<tf2_ros::TransformBroadcaster>(this);
        // 把成员函数当做回调函数，使用函数包装器 std::bind(&类::成员函数, 对象指针)
        _timer = this->create_wall_timer(100ms, std::bind(&TFBroadcaster::publish_tf, this));
        this->publish_tf();
    }

    void publish_tf()
    {
        geometry_msgs::msg::TransformStamped transform;
        transform.header.stamp = this->get_clock()->now();
        transform.header.frame_id = "map";
        transform.child_frame_id = "base_link";

        transform.transform.translation.x = 2.0;  // 单位是 米
        transform.transform.translation.y = 3.0;
        transform.transform.translation.z = 0.0;
        
        tf2::Quaternion q;
        q.setRPY(0.0, 0.0, 30.0*M_PI/180.0);  // 60.0*M_PI/180.0  弧度转角度【*M_PI】，再转弧度【/180.0】

        transform.transform.rotation = tf2::toMsg(q);

        this->_broadcaster->sendTransform(transform);
    }
};

int main(int argc, char* argv[])
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<TFBroadcaster>("dynamic_tf_broadcaster");
    rclcpp::spin(node);
    rclcpp::shutdown();

    return 0;
}