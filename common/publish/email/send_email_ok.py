#!/usr/bin/env python
#coding: utf-8

import sys
import json
import requests
from send_email import send_email_from_moscow

reload(sys)
sys.setdefaultencoding("utf-8")

page = sys.argv[1]
branch = sys.argv[2]

try:
  with open("build/data/builds_current.json") as json_data:
    builds_current = json.load(json_data)
except IOError as e:
  print "Error: File not found \"build/data/builds_current.json\""
  exit()

def stand_comparator(left, right):
  if left == "shell":
    return -1
  elif right == "shell":
    return 1
  elif left == "online":
    return 1
  elif right == "online":
    return -1
  elif left == "qatar":
    return -1
  elif right == "qatar":
    return 1
  else:
    return 0

stands = []

for stand in builds_current[branch]:
  stands.append(stand)

stands.sort(stand_comparator)

email_json = {}

for stand in stands:
  for mode in builds_current[branch][stand]:
    for platform in builds_current[branch][stand][mode]:
      merged_merge_request_list = builds_current[branch][stand][mode][platform]["merged_merge_request_list"]
      opened_merge_request_list = builds_current[branch][stand][mode][platform]["opened_merge_request_list"]

      msg = "<br>"
      if len(merged_merge_request_list) > 0:
        msg += "Исправления, вошедшие в сборки:<br>"
        for merge_request in merged_merge_request_list:
          msg += merge_request + "<br>"
          if len(opened_merge_request_list) > 0:
            msg += "<br>"
      else:
        msg += "Новых исправлений нет<br>"
        if len(opened_merge_request_list) > 0:
          msg += "<br>"

      if len(opened_merge_request_list) > 0:
        msg += "Исправления, ожидающие включения в сборки:<br>"
        for merge_request in opened_merge_request_list:
          msg += merge_request + "<br>"

      if msg not in email_json:
        email_json[msg] = ""
      data_stand = email_json[msg].strip().split("</br>")[len(email_json[msg].strip().split("</br>")) - 1]
      if stand not in data_stand:
        email_json[msg] += stand + ": " + mode + " - " + platform
      elif mode not in data_stand:
        email_json[msg] += "; " + mode + " - " + platform
      else:
        email_json[msg] += ", " + platform

      revision = builds_current[branch][stand][mode][platform]["revision"]
  email_json[msg] += "</br>"

message = "<b>Ветка " + branch + ", ревизия " + revision + "</b><br>"

for msg in email_json:
  message += "<br>" + email_json[msg] + msg + "---------------------------------------------------------------------------------------------------------------------------------------------------------------<br>"

message += "<br>В конфлюенсе: http://confluence/pages/viewpage.action?pageId=" + page

from_address = "falshtynsky@softlab.ru"
to_addresses = "falshtynsky@softlab.ru"
to_addresses += ""
cc_addresses = ""
subject = "РСХБ_МБЮЛ. Сборки"
message = message.encode("utf-8")

send_email_from_moscow(from_address, to_addresses, cc_addresses, subject, message, "html")
