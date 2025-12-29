#include <iostream>
#include <memory>

int main(int argc, char** argv)
{
    auto p1 = std::make_shared<std::string>("this is a str");
    std::cout << "p1 的引用计数：" << p1.use_count() << ", 指向内存地址：" << p1.get() << std::endl;

    auto p2 = p1;
    std::cout << "p1 的引用计数：" << p1.use_count() << ", 指向内存地址：" << p1.get() << std::endl;
    std::cout << "p2 的引用计数：" << p2.use_count() << ", 指向内存地址：" << p2.get() << std::endl;

    p1.reset();  // 释放引用，不指向 "this is a str" 所在内存了
    std::cout << "p1 的引用计数：" << p1.use_count() << ", 指向内存地址：" << p1.get() << std::endl;
    std::cout << "p2 的引用计数：" << p2.use_count() << ", 指向内存地址：" << p2.get() << std::endl;

    std::cout << "p2 的指向内存地址数据：" << p2->c_str() << std::endl;


    return 0;
}