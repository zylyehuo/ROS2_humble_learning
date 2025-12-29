#include <iostream>
#include <algorithm>

int main(int argc, char **argv)
{
    auto add = [](int a, int b) -> int  // [捕获参数](设置需要的参数) -> 返回类型
    { 
        return a + b; 
    };

    int sum = add(200, 50);

    auto print_sum = [sum]() -> void
    {
        std::cout << sum << std::endl;
    };

    print_sum();
    
    return 0;
}
