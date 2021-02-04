import smtplib
from config import receiver
from email.utils import formataddr
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class autoemail:

    def __init__(self):
        self.reset()

    def reset(self):
        self.context = "自动化值班通知:\n"

    def build_msg(self, txt):
        self.context += f"{txt}\n"
    
    def send(self):
        server = smtplib.SMTP_SSL("smtp.qq.com", 465)
        server.login('754587525@qq.com', 'brujwzwtbwjxbcfb')
        msg=MIMEText(self.context, 'plain', 'utf-8')
        msg['From'] = formataddr(["自动化值班", '754587525@qq.com'])
        msg['To']=formataddr(["值班人",receiver])
        server.sendmail('754587525@qq.com',[receiver,],msg.as_string())
        server.quit()
        self.reset()