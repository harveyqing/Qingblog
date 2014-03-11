# -*- coding: utf-8 -*-
r"""
    account
    ~~~~~~~

    Utility for account control.

    :copyright: (c) 2013 by Harvey Wang.
"""

import time
import base64
import hashlib
import functools
from flask import current_app, g, request, session
from flask import url_for, redirect
from ..models import User


class require_role(object):

    def __init__(self, role):
        self.role = role

    def __call__(self, method):
        @functools.wraps(method)
        def wrapper(*args, **kwargs):
            if not g.user:  # 尚未登录
                url = url_for('account.signin')
                if '?' not in url:
                    url += '?next=' + request.url  # 记录下当前的url，以便登录后跳转
                return redirect(url)
            if g.user.role == 'admin':
                # this is superuser, have no limitation
                return method(*args, **kwargs)

            return method(*args, **kwargs)
        return wrapper

require_admin = require_role('admin')


# 获取当前浏览页面用户
def get_current_user():
    if 'uid' in session and 'token' in session:
        user = User.query.filter_by(uid=session['uid']).first()
        if not user:
            return None
        if user.token != session['token']:
            return None
        return user
    return None


# 登录指定用户
def login_user(user, permanent=False):
    if not user:
        return None
    session['uid'] = user.uid
    session['token'] = user.token
    if permanent:
        session.permanent = True
    return user


# 登出当前用户
def logout_user():
    if 'uid' not in session:
        return
    session.pop('uid')
    session.pop('token')


# 创建认证口令
def create_auth_token(user):
    timestamp = int(time.time())
    secret = current_app.secret_key
    token = '%s%s%s%s' % (secret, timestamp, user.uid, user.token)
    hsh = hashlib.sha1(token).hexdigest()
    return base64.b32encode('%s|%s%s' % (timestamp, user.uid, hsh))


# 口令验证
def verify_auth_token(token, expires=30):
    try:
        token = base64.b32decode(token)
    except:
        return None
    bits = token.split('|')
    if len(bits) != 3:
        return None
    timestamp, user_uid, hsh = bits
    try:
        timestamp = int(timestamp)
        user_uid = int(user_uid)
    except:
        return None
    delta = time.time() - timestamp
    if delta < 0:
        return None
    user = User.query.get(user_uid)
    if not user:
        return None
    secret = current_app.secret_key
    _hsh = hashlib.sha1('%s%s%s%s' % (secret, timestamp, user_uid, user.token))
    if hsh == _hsh.hexdigest():
        return user
    return None
