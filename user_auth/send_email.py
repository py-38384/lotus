"""
You need a email account with less secure login enable
best, if use a google account with app password
"""
import smtplib
from email.mime.text import MIMEText
from email.message import Message
def send_email(
        sender_email,
        receiver_email,
        sender_account_pass,
        mail_subject,
        email_body,
        smtp_server='smtp.gmail.com',
        smtp_port=587):

    message = Message()
    message["Subject"] = mail_subject
    message["From"] = sender_email
    message["To"] = receiver_email
    message.add_header('Content-Type','text/html')
    message.set_payload(email_body)
    server = smtplib.SMTP(smtp_server,smtp_port)
    server.starttls()
    server.login(sender_email, sender_account_pass)
    try:
        server.sendmail(sender_email,receiver_email,message.as_string())
        return True
    except Exception as e:
        return 'Email not send. ERORR!!! -> {0}'.format(e)
    
