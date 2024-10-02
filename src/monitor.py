from .email_utils import send_alert_email  # 使用相对导入
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
import threading
import time
import datetime
import os
import sys

class Monitor:
    def __init__(self, url, interval, keyword, log_directory='logs'):
        self.url = url
        self.interval = interval
        self.keyword = keyword
        self.monitoring = False
        self.driver = None
        self.log_directory = log_directory

        if not os.path.exists(self.log_directory):
            os.makedirs(self.log_directory)
        print(f"日志目录: {os.path.abspath(self.log_directory)}")
        print(f"当前工作目录: {os.getcwd()}")
        print(f"Python 版本: {sys.version}")
        print(f"Selenium 版本: {webdriver.__version__}")

    def start(self):
        if not self.monitoring:
            self.monitoring = True
            threading.Thread(target=self.monitor, daemon=True).start()
            print("监控线程已启动")

    def pause(self):
        if self.monitoring:
            self.monitoring = False
            if self.driver:
                self.driver.quit()
                self.driver = None
            print("监控已暂停")

    def monitor(self):
        options = Options()
        options.headless = True
        
        try:
            service = Service(GeckoDriverManager().install())
            self.driver = webdriver.Firefox(service=service, options=options)
            print("Firefox WebDriver 已初始化")
        except Exception as e:
            print(f"初始化 WebDriver 时发生错误: {e}")
            self.monitoring = False
            return

        while self.monitoring:
            try:
                print(f"正在访问 URL: {self.url}")
                self.driver.get(self.url)
                time.sleep(5)  # 等待页面加载

                page_text = self.driver.find_element("tag name", "body").text
                print("已获取页面内容")
                self.save_log(page_text)

                if self.keyword in page_text:
                    print(f"检测到关键词: {self.keyword}")
                    self.alert(self.keyword)
                else:
                    print(f"未检测到关键词: {self.keyword}")

                print(f"等待 {self.interval} 秒后进行下一次检查...")
                time.sleep(self.interval)
            except Exception as e:
                print(f"监控过程中发生错误: {e}")
                self.monitoring = False
                if self.driver:
                    self.driver.quit()
                    self.driver = None
                messagebox.showerror("监测错误", str(e))

    def save_log(self, page_text):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        log_filename = f"page_{timestamp}.txt"
        log_path = os.path.join(self.log_directory, log_filename)
        try:
            with open(log_path, "w", encoding='utf-8') as file:
                file.write(page_text)
            print(f"日志已保存: {log_path}")
        except Exception as e:
            print(f"保存日志失败: {e}")

    def alert(self, keyword):
        print(f"检测到关键词: {keyword}")
        messagebox.showwarning("关键词检测", f"检测到关键词: {keyword}")
        send_alert_email(keyword, self.url)

    def get_latest_log(self):
        try:
            files = sorted(
                [f for f in os.listdir(self.log_directory) if f.startswith('page_') and f.endswith('.txt')],
                reverse=True
            )
            if not files:
                return "没有找到日志文件。"
            latest_file = files[0]
            with open(os.path.join(self.log_directory, latest_file), 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            return f"读取日志失败: {e}"