#ifndef NAV2_CUSTOM_PLANNER__NAV2_CUSTOM_PLANNER_HPP_
#define NAV2_CUSTOM_PLANNER__NAV2_CUSTOM_PLANNER_HPP_

#include <memory>
#include <string>

// 消息接口
#include "geometry_msgs/msg/point.hpp"  // 点的接口
#include "geometry_msgs/msg/pose_stamped.hpp"  // 位置接口
#include "nav_msgs/msg/path.hpp"  // 路径接口
#include "nav2_costmap_2d/costmap_2d_ros.hpp"  // 包含了 #include "nav_msgs/msg/occupancy_grid.hpp"，栅格地图接口

#include "nav2_core/global_planner.hpp"  // 全局规划器，提供基类 nav2_core::GlobalPlanner
#include "nav2_util/lifecycle_node.hpp"  // rclcpp 的子类，已经引入了 #include "rclcpp/rclcpp.hpp"
#include "nav2_util/robot_utils.hpp"  // 常用工具

namespace nav2_custom_planner {
  // 自定义导航规划器类
  class CustomPlanner : public nav2_core::GlobalPlanner {
    public:
      CustomPlanner() = default;
      ~CustomPlanner() = default;
      // 纯虚函数需要全部（五个）在类中重写
      // 插件配置方法
      void configure(
          const rclcpp_lifecycle::LifecycleNode::WeakPtr &parent, std::string name,
          std::shared_ptr<tf2_ros::Buffer> tf,
          std::shared_ptr<nav2_costmap_2d::Costmap2DROS> costmap_ros
      ) override;
      // 插件清理方法
      void cleanup() override;
      // 插件激活方法
      void activate() override;
      // 插件停用方法
      void deactivate() override;
      // 为给定的起始和目标位姿创建路径的方法
      nav_msgs::msg::Path createPlan(const geometry_msgs::msg::PoseStamped &start, const geometry_msgs::msg::PoseStamped &goal) override;

    private:
      // 坐标变换缓存指针，可用于查询坐标关系
      std::shared_ptr<tf2_ros::Buffer> tf_;
      // 节点指针
      nav2_util::LifecycleNode::SharedPtr node_;
      // 全局代价地图
      nav2_costmap_2d::Costmap2D *costmap_;
      // 全局代价地图的坐标系的名字，插件名字
      std::string global_frame_, name_;
      // 插值分辨率
      double interpolation_resolution_;
  };

} // namespace nav2_custom_planner

#endif // NAV2_CUSTOM_PLANNER__NAV2_CUSTOM_PLANNER_HPP_