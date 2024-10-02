import smtplib
from email.mime.text import MIMEText
from .config import EMAIL_ADDRESS, EMAIL_PASSWORD, SMTP_SERVER, SMTP_PORT, RECIPIENT_EMAIL  # 使用相对导入

def send_alert_email(keyword, url):
    subject = '网页监测告警'
    body = f"在监测的页面 {url} 中检测到关键词: {keyword}"
    
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = RECIPIENT_EMAIL
    
    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:  # 使用 SMTP_SSL 适用于端口 465
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
        print("告警邮件已发送")
    except Exception as e:
        print(f"发送邮件失败: {e}")