import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import dotenv
from celery import Celery

celery = Celery('server', broker='redis://127.0.0.1:6379')
dotenv.load_dotenv()
SECRET = os.environ.get('SECRET')
EMAIL_SENDER = os.environ.get('EMAIL_SENDER')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
HOST = os.environ.get('HOST')

# Отправка кода на почту при регистрации
#@celery.task
def send_code(email, name, surname, password, number):
    email_sender = EMAIL_SENDER
    email_password = EMAIL_PASSWORD
    email_getter = email
    smtp_server = smtplib.SMTP('smtp.yandex.ru', 587)
    smtp_server.starttls()
    msg = MIMEMultipart()
    msg.attach(MIMEText(
        f"Здравствуйте {name} {surname}!\nВаш логин - {email}\nПароль - {password}\nДля продолжения введите проверочный код регистрации на сайте ToDo - {str(number)}\n Ссылка на сайт - {HOST}"))
    msg["From"] = email_sender
    msg["Subject"] = "Код подтверждения регистрации на сайте ToDo"
    smtp_server.set_debuglevel(1)
    smtp_server.login(email_sender, email_password)
    smtp_server.sendmail(email_sender, email_getter, msg.as_string())
    smtp_server.quit()

# Отправка кода на почту при создании админом
#@celery.task
def send_code_staff(email, name, surname, password):
    email_sender = EMAIL_SENDER
    email_password = EMAIL_PASSWORD
    email_getter = email
    smtp_server = smtplib.SMTP('smtp.yandex.ru', 587)
    smtp_server.starttls()
    msg = MIMEMultipart()
    msg.attach(MIMEText(
        f"Здравствуйте {name} {surname}!\nВаш логин - {email}\nПароль - {password}\n Ссылка на сайт - {HOST}"))
    msg["From"] = email_sender
    msg["Subject"] = "Данные авторизации на сайте ToDo"
    smtp_server.set_debuglevel(1)
    smtp_server.login(email_sender, email_password)
    smtp_server.sendmail(email_sender, email_getter, msg.as_string())
    smtp_server.quit()
