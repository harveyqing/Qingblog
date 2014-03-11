# -*- coding: utf-8 -*-
r"""
    mail
    ~~~~~~~

    Utility for seding mail.

    :copyright: (c) 2014 by Harvey Wang.
"""

from flask.ext.mail import Mail, Message
from threading import Thread


def send_async_mail(msg):
    mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    thr = Thread(target=send_async_mail, args=[msg])
    thr.start()


mail = Mail()
