#include <iostream>
#include <thread>  // 多线程
#include <chrono>  // 时间相关
#include <functional>  // 函数包装器
#include "cpp-httplib/httplib.h"  // 下载相关

class Downloder
{
private:
    /* data */
public:
    // void download(域名， 路径， 回调函数(地址， 内容));
    void download(const std::string &host, const std::string &path, const std::function<void(const std::string &, const std::string &)> &callback_word_count)
    {
        std::cout << "线程编号：" << std::this_thread::get_id() << std::endl;
        httplib::Client client(host);
        auto response = client.Get(path);
        if(response && response->status==200)
        {
            callback_word_count(path, response->body);
        }
    };

    // void start_download(域名， 路径， 回调函数(地址， 内容));
    void start_download(const std::string &host, const std::string &path, const std::function<void(const std::string &, const std::string &)> &callback_word_count)
    {
        // auto download_func = std::bind(函数的模板地址, 当前对象的指针, 函数参数的占位符[此处 download 要有三个参数]);
        auto download_func = std::bind(&Downloder::download, this, std::placeholders::_1, std::placeholders::_2, std::placeholders::_3);
        std::thread thread(download_func, host, path, callback_word_count);
        thread.detach();  // 防止阻塞线程，detach 进行线程分离
    };
};

int main(int argc, char** argv)
{
    auto downloader = Downloder();

    // 字符数量计算
    auto word_count = [](const std::string &path, const std::string &result) -> void
    {
        std::cout << "下载完成" << path << result.length() << result.substr(0, 9) << std::endl;
    };

    downloader.start_download("http://localhost:8000", "/novel1.txt", word_count);
    downloader.start_download("http://localhost:8000", "/novel2.txt", word_count);
    downloader.start_download("http://localhost:8000", "/novel3.txt", word_count);

    // 休眠 10 秒
    std::this_thread::sleep_for(std::chrono::milliseconds(1000*10));
    return 0;
}



