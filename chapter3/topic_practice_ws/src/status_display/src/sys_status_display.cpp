#include <QApplication>
#include <QLabel>
#include <QString>
#include <rclcpp/rclcpp.hpp>
#include "status_interfaces/msg/system_status.hpp"

using SystemStatus = status_interfaces::msg::SystemStatus;

class SysStatusDisplay : public rclcpp::Node
{
private:
    rclcpp::Subscription<SystemStatus>::SharedPtr _subscriber;
    QLabel* _label;

public:
    SysStatusDisplay():Node("sys_status_display")
    {
        _label = new QLabel();
        _subscriber = this->create_subscription<SystemStatus>("sys_status", 10, 
                    [&](const SystemStatus::SharedPtr msg)->void
                    {
                        _label->setText(get_qstr_from_msg(msg));
                    });
        _label->setText(get_qstr_from_msg(std::make_shared<SystemStatus>()));
        _label->show();
    };

    QString get_qstr_from_msg(const SystemStatus::SharedPtr msg)
    {
        /* 
        msg.stamp = self.get_clock().now().to_msg()  # 获取当前的时间
        msg.host_name = platform.node()  # 主机名字
        msg.cpu_percent = cpu_percent
        msg.memory_percent = memory_info.percent
        msg.memory_total = memory_info.total / 1024 / 1024  # b -> kb -> Mb
        msg.memory_available = memory_info.available / 1024 / 1024
        msg.net_sent = net_io_counters.bytes_sent / 1024 / 1024
        msg.net_recv = net_io_counters.bytes_recv / 1024 / 1024
        */
        std::stringstream show_str;
        show_str << 
        "==========系统状态可视化显示工具==========\n" <<
        "数 据 时 间:\t" << msg->stamp.sec << "\ts\n" <<
        "主 机 名 字:\t" << msg->host_name << "\ts\n" <<
        "CPU 使用率:\t" << msg->cpu_percent << "\t%\n" <<
        "内存使用率:\t" << msg->memory_percent << "\t%\n" <<
        "内存总大小:\t" << msg->memory_total << "\tMb\n" <<
        "剩余可用内存:\t" << msg->memory_available << "\tMb\n" <<
        "网络发送量:\t" << msg->net_sent << "\tMb\n" <<
        "网络接收量:\t" << msg->net_recv << "\tMb\n" <<
        "=========================================";
        return QString::fromStdString(show_str.str());
    }
};

int main(int argc, char* argv[])
{
    rclcpp::init(argc, argv);

    QApplication app(argc, argv);

    auto node = std::make_shared<SysStatusDisplay>();

    std::thread spin_thread([&]()->void
                            {
                                rclcpp::spin(node);    // 阻塞代码
                            });
    
    spin_thread.detach();

    app.exec();  // 执行应用，阻塞代码

    rclcpp::shutdown();

    return 0;
}
