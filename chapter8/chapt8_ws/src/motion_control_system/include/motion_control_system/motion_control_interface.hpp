#ifndef MOTION_CONTROL_INTERFACE_HPP  // 宏定义，防止头文件被多次包含（造成重复定义）
#define MOTION_CONTROL_INTERFACE_HPP

namespace motion_control_system {
    class MotionController {
        public:
            virtual void start() = 0;  // 有了纯虚函数，代表这是一个抽象类
            virtual void stop() = 0;
    };
}  // namespace motion_control_system

#endif  // MOTION_CONTROL_INTERFACE_HPP