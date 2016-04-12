#!/bin/env python
# -*- coding: UTF-8 -*-
#
# (c) Chiara Malagoli
#
# v 0.0.1.2
#
# file: mailmetheerror.py
# auth: Chiara Malagoli <malagoli@gbinside.com>
# desc:
#
# $Id: mailmetheerror.py 2016/04/12 23.56.00 chiara $
# --------------

import sys
import traceback

FROM = 'ircbot@gbinside.com'
TO = 'malagoli@gbinside.com'
SMTP = 'localhost'


def mail(sb, text):
    try:
        import smtplib
        from email.MIMEText import MIMEText
        msg = MIMEText(text)
        msg['From'] = FROM
        msg['To'] = TO
        msg['Subject'] = 'Error from ' + sb
        s = smtplib.SMTP()
        s.connect(SMTP)
        s.sendmail(FROM, TO, msg.as_string())
        s.close()
    except:  # I know, too broad exception
        pass


def install_excepthook():
    def my_excepthook(exctype, value, tb):
        text = ''.join(traceback.format_exception(exctype, value, tb))
        mail(str(sys.argv[0]), text)
        print text

    sys.excepthook = my_excepthook


install_excepthook()

if __name__ == "__main__":
    mail(__file__, 'Test')
