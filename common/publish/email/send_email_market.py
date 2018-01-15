#!/usr/bin/env python
#coding: utf-8

import sys
from send_email import send_email_from_moscow

reload(sys)
sys.setdefaultencoding("utf-8")

message = sys.argv[1]

from_address = "falshtynsky@softlab.ru"
to_addresses = "falshtynsky@softlab.ru"
subject = "РСХБ_МБЮЛ. Сборки market"

send_email_from_moscow(from_address, to_addresses, "", subject, message, "html")
