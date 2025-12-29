#include <iostream>
#include <functional> // 函数包装器头文件

// 自由函数
void save_with_free_func(const std::string &file_name)
{
    std::cout << "自由函数：" << file_name << std::endl;
}

// 成员函数
class FileSave
{
private:
    /* data */
public:
    FileSave(/* args */) = default;
    ~FileSave() = default;

    void save_with_member_func(const std::string &file_name)
    {
        std::cout << "成员方法：" << file_name << std::endl;
    };
};

int main(int argc, char **argv)
{
    FileSave file_save;

    // Lambda 函数
    auto save_with_lambda_func = [](const std::string &file_name) -> void
    {
        std::cout << "Lambda 函数：" << file_name << std::endl;
    };

    // save_with_free_func("file.txt");
    // file_save.save_with_member_func("file.txt");
    // save_with_lambda_func("file.txt");

    std::function<void(const std::string &)> save1 = save_with_free_func;
    std::function<void(const std::string &)> save2 = std::bind(&FileSave::save_with_member_func, &file_save, std::placeholders::_1);
    std::function<void(const std::string &)> save3 = save_with_lambda_func;

    // 通过函数包装器实现了统一的调用方法
    save1("file.txt");
    save2("file.txt");
    save3("file.txt");

    return 0;
}
