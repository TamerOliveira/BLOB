import smtplib
import ssl
from email.message import EmailMessage
import os

class Email:
    def __init__(self, receiver:str, subject:str, body:str):
        self.email_sender = 'caiolexrock@gmail.com'
        self.email_password = os.environ.get('EMAIL_PASSWORD')
        self.email_receiver = receiver
        self.subject = subject
        self.body = body

    def enviar(self):
        e_mail = EmailMessage()
        e_mail['From'] = self.email_sender
        e_mail['To'] = self.email_receiver
        e_mail['Subject'] = self.subject
        e_mail.set_content(self.body)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(self.email_sender, self.email_password)
            smtp.sendmail(self.email_sender, self.email_receiver, e_mail.as_string())
