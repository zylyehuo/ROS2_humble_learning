#include "iostream"

int main(int argc, char** argv)  // 设置入口参数
{
    std::cout << "参数数量=" << argc << std::endl;
    std::cout << "程序名字=" << argv[0] << std::endl;

    std::string arg1 = argv[1];
    if(arg1 == "--help")
    {
        std::cout << "这是程序帮助，但是没有什么用" << argv[0] << std::endl;
    }
    return 0;
}