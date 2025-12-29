import threading
import requests

"""
# 准备小说数据，并启动一个本地服务器
zylyehuo@LAPTOP-4FQQUA1G:~/ROS2_learning/chapter2/chapter2.5/chapt2_ws$ echo "第一章 少年踏上修仙路" > novel1.txt
zylyehuo@LAPTOP-4FQQUA1G:~/ROS2_learning/chapter2/chapter2.5/chapt2_ws$ echo "第二章 学习修仙，马上升天" > novel2.txt
zylyehuo@LAPTOP-4FQQUA1G:~/ROS2_learning/chapter2/chapter2.5/chapt2_ws$ echo "第三章 修仙界，位列仙班" > novel3.txt
zylyehuo@LAPTOP-4FQQUA1G:~/ROS2_learning/chapter2/chapter2.5/chapt2_ws$ python3 -m http.server
""" 
class Downloader:
    def download(self, url, callback_word_count):
        print(f"线程编号：{threading.get_ident()} 开始下载：{url}")
        response = requests.get(url)
        response.encoding = 'utf-8'
        callback_word_count(url, response.text)  # 调用回调函数
    
    def start_download(self, url, callback_word_count):
        # self.download(url, callback_word_count)
        thread = threading.Thread(target=self.download, args=(url, callback_word_count))  # 创建线程
        thread.start()  # 启动线程
    
def word_count(url, result):
    """
    普通函数，用于回调
    """
    print(f"{url}:{len(result)}->{result[:5]}")
    
def main():
    downloader = Downloader()
    
    downloader.start_download("http://localhost:8000/novel1.txt", word_count)
    downloader.start_download("http://localhost:8000/novel2.txt", word_count)
    downloader.start_download("http://localhost:8000/novel3.txt", word_count)