import os
from dotenv import load_dotenv

load_dotenv()  # 加载 .env 文件

# 从环境变量中读取邮箱配置信息
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
SMTP_SERVER = os.getenv('SMTP_SERVER')
SMTP_PORT = int(os.getenv('SMTP_PORT', 587))  # 默认使用587端口
RECIPIENT_EMAIL = os.getenv('RECIPIENT_EMAIL', 'cdutboy928@gmail.com')