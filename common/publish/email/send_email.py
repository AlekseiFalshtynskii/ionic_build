#!/usr/bin/env python
#coding: utf-8

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

def send_email_from_vologda(from_address, to_addresses, cc_addresses, subject, message, type):
  msg = MIMEMultipart()
  msg["From"] = from_address
  msg["To"] = to_addresses
  msg["Cc"] = cc_addresses
  msg["Subject"] = subject
  msg.attach(MIMEText(message, type))
  text = msg.as_string()
  server = smtplib.SMTP("172.16.1.0", 25)
  server.sendmail(from_address, to_addresses.split(",") + cc_addresses.split(","), text)
  server.quit()

def send_email_from_moscow(from_address, to_addresses, cc_addresses, subject, message, type):
  msg = MIMEMultipart()
  msg["From"] = from_address
  msg["To"] = to_addresses
  msg["Cc"] = cc_addresses
  msg["Subject"] = subject
  msg.attach(MIMEText(message, type))
  text = msg.as_string()
  server = smtplib.SMTP("172.16.3.70", 25)
  server.ehlo()
  server.set_debuglevel(1)
  server.starttls()
  server.ehlo()
  server.login("Login", "Password")
  server.sendmail(from_address, to_addresses.split(",") + cc_addresses.split(","), text)
  server.quit()
