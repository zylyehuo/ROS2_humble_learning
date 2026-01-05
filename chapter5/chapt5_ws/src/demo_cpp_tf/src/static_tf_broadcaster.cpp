#include "rclcpp/rclcpp.hpp"
#include "geometry_msgs/msg/transform_stamped.hpp"  // 提供消息接口
#include "tf2/LinearMath/Quaternion.hpp"  // 提供 tf2::Quaternion 类
#include "tf2_geometry_msgs/tf2_geometry_msgs.hpp"  // 消息类型转换函数
#include "tf2_ros/static_transform_broadcaster.hpp"  // 静态坐标广播器

/*
ros2 topic list

ros2 topic echo /tf_static

ros2 topic info /tf_static -v

ros2 run tf2_ros tf2_echo map target_point
*/

class StaticTFBroadcaster: public rclcpp::Node
{
private:
    std::shared_ptr<tf2_ros::StaticTransformBroadcaster> _broadcaster;

public:
    StaticTFBroadcaster(std::string node_name): Node(node_name)
    {
        _broadcaster = std::make_shared<tf2_ros::StaticTransformBroadcaster>(this);
        this->publish_tf();
    }

    void publish_tf()
    {
        geometry_msgs::msg::TransformStamped transform;
        transform.header.stamp = this->get_clock()->now();
        transform.header.frame_id = "map";
        transform.child_frame_id = "target_point";

        transform.transform.translation.x = 5.0;  // 单位是 米
        transform.transform.translation.y = 3.0;
        transform.transform.translation.z = 0.0;
        
        tf2::Quaternion q;
        q.setRPY(0.0, 0.0, 60.0*M_PI/180.0);  // 60.0*M_PI/180.0  弧度转角度【*M_PI】，再转弧度【/180.0】

        transform.transform.rotation = tf2::toMsg(q);

        this->_broadcaster->sendTransform(transform);
    }
};

int main(int argc, char* argv[])
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<StaticTFBroadcaster>("static_tf_broadcaster");
    rclcpp::spin(node);
    rclcpp::shutdown();

    return 0;
}