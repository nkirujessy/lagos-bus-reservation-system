import math
import random

import app
from app.models.settingsmodel import settings
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def app_config():

 return settings.query.first()

def app_send_email(email,subject,message):

 try:
  app_email= app_config().email
  app_password= app_config().password
  host= app_config().host
  port= app_config().port

  mail = MIMEMultipart("alternative")
  mail["Subject"] = subject
  mail["From"] = app_config().email
  mail["To"] = email
  mail.attach(MIMEText(message, "html"))
  mailer = smtplib.SMTP_SSL(host, port)
  mailer.ehlo()
  mailer.login(app_email, app_password)
  mailer.sendmail(app_email, email, mail.as_string())
  mailer.close()
  return  mailer
 except NameError:
  raise Exception(NameError)

def generateOTP() :
  digits = "0123456789"
  OTP = ""
  for i in range(4) :
   OTP += digits[math.floor(random.random() * 10)]

  return OTP

