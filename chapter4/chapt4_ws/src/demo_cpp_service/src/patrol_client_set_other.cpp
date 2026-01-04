#include <rclcpp/rclcpp.hpp>
#include "chapt4_interfaces/srv/patrol.hpp"
#include <chrono>
#include <ctime>
#include "rcl_interfaces/msg/parameter.hpp"
#include "rcl_interfaces/msg/parameter_value.hpp"
#include "rcl_interfaces/msg/parameter_type.hpp"
#include "rcl_interfaces/srv/set_parameters.hpp"

using SetParam = rcl_interfaces::srv::SetParameters;
using namespace std::chrono_literals;  // 可以使用 10s 100ms
using Patrol = chapt4_interfaces::srv::Patrol;

class PatrolClient : public rclcpp::Node
{
private:
    rclcpp::TimerBase::SharedPtr _timer;  // 定时器
    rclcpp::Client<Patrol>::SharedPtr _patrol_client;  //  创建客户端

public:
    explicit PatrolClient(const std::string &node_name) : Node(node_name) // explicit 防止隐式构造对象，提高代码可维护性
    {
        _patrol_client = this->create_client<Patrol>("patrol");
        _timer = this->create_wall_timer(10s, [&]()->void{
            // 检测服务端是否上线
            while(!this->_patrol_client->wait_for_service(1s))
            {
                if(!rclcpp::ok())
                {
                    RCLCPP_ERROR(this->get_logger(), "等待服务上线过程中, rclcpp已退出");
                    return;
                }
                RCLCPP_INFO(this->get_logger(), "等待服务上线中");
                srand(time(NULL));  // 初始化随机数种子
            }

            // 构造请求对象
            auto request = std::make_shared<Patrol::Request>();
            request->target_x = rand() % 15;
            request->target_y = rand() % 15;
            RCLCPP_INFO(this->get_logger(), "目标点设置为：%f, %f", request->target_x, request->target_y);

            // 发送请求
            this->_patrol_client->async_send_request(request, [&](rclcpp::Client<Patrol>::SharedFuture result_future)->void{
                auto response = result_future.get();
                if(response->result == Patrol::Response::SUCESS)
                {
                    RCLCPP_INFO(this->get_logger(), "请求巡逻目标点成功");
                }
                else
                {
                    RCLCPP_INFO(this->get_logger(), "请求巡逻目标点失败");
                }
            });
        });
    }

    // 创建客户端，发送请求，返回结果
    SetParam::Response::SharedPtr call_set_parameter(const rcl_interfaces::msg::Parameter &param)
    {
        auto _param_client = this->create_client<SetParam>("/turtle_control/set_parameters");

        // 检测服务端是否上线
        while(!_param_client->wait_for_service(1s))
        {
            if(!rclcpp::ok())
            {
                RCLCPP_ERROR(this->get_logger(), "等待服务上线过程中, rclcpp已退出");
                return nullptr;
            }
            RCLCPP_INFO(this->get_logger(), "等待服务上线中");
        }

        // 构造请求对象
        auto request = std::make_shared<SetParam::Request>();
        request->parameters.push_back(param);


        // 发送请求
        auto future = _param_client->async_send_request(request);
        rclcpp::spin_until_future_complete(this->get_node_base_interface(), future);

        // 获取响应
        auto response = future.get();

        return response;
    }

    // 更新参数 _k
    void update_server_param_k(double k)
    {
        // 创建参数对象
        auto param = rcl_interfaces::msg::Parameter();
        param.name = "_k";

        // 创建参数值
        auto param_value = rcl_interfaces::msg::ParameterValue();
        param_value.type = rcl_interfaces::msg::ParameterType::PARAMETER_DOUBLE;
        param_value.double_value = k;
        param.value = param_value;

        // 请求更新参数，并处理
        auto response = this->call_set_parameter(param);

        if(response == NULL)
        {
            RCLCPP_INFO(this->get_logger(), "参数更新失败");
            return;
        }

        for(auto result:response->results)
        {
            if(result.successful == false)
            {
                RCLCPP_INFO(this->get_logger(), "参数更新失败，原因：%s", result.reason.c_str());
                return;
            }
            else
            {
                RCLCPP_INFO(this->get_logger(), "参数更新成功");
            }
        }
    }
};

int main(int argc, char *argv[])
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<PatrolClient>("patrol_client");

    node->update_server_param_k(3.0);

    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}