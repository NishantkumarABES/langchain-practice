import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate

class Email:
    def __init__(self, sender_email, sender_password, sender_name=None):
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.sender_name = sender_name or sender_email  
        
    def start_server(self):
        self.server = smtplib.SMTP('smtp.gmail.com', 587)
        self.server.starttls()
        self.server.login(self.sender_email, self.sender_password)

    def send_email(self, recipient_email, subject, body):
        msg = MIMEMultipart('related')
        sender_info = f"{self.sender_name} <{self.sender_email}>"
        msg['From'] = sender_info 
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg['Date'] = formatdate(localtime=True)

        msg.attach(MIMEText(body, 'html'))
        self.server.sendmail(self.sender_email, recipient_email, msg.as_string())  
        return "success"
    def close_connection(self):
        self.server.quit()

    
    

        

