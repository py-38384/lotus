import smtplib
from email.mime.text import MIMEText
from email.message import Message
def send_email(sender_email='workwithpiyal@gmail.com',receiver_email='piyal13133@gmail.com',sender_google_account_pass='wrgp kqoh cqtq hagv',mail_subject="testing purpose",has_email_body=True,file_path='emails/email_body',email_body="this is a basic email", smtp_server='smtp.gmail.com', smtp_port=587):
    file = False
    if has_email_body:
        file = open(file_path,'rb') #importing email body which content HTML,CSS AND Javascript
    
    mail_body = file.read()


    message = Message()
    message["Subject"] = mail_subject
    message["From"] = sender_email
    message["To"] = receiver_email
    message.add_header('Content-Type','text/html')
    if has_email_body:
        message.set_payload(mail_body)
    else:
        message.set_payload(email_body)
    server = smtplib.SMTP(smtp_server,587)
    server.starttls()
    server.login(sender_email, sender_google_account_pass)
    try:
        server.sendmail(sender_email,receiver_email,message.as_string())
        return 'Email Successfully send'
    except Exception as e:
        return 'Email not send. ERORR!!! -> {0}'.format(e)
    
