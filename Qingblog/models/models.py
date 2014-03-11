# -*- coding: utf-8 -*-
r"""
    models
    ~~~~~~~

    Data model of blog.

    :copyright: (c) 2013 by Harvey Wang.
"""

import re
from datetime import datetime
from werkzeug import security
from ._base import db, SessionMixin

__all__ = [
    'Category', 'Tag',
    'Article', 'Comment',
    'User', 'Link',
    'BlackList', 'Subscriber',
    'article_tags']

article_tags = db.Table(
    'tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.tid')),
    db.Column('article_id', db.Integer, db.ForeignKey('article.aid')))


class Category(db.Model, SessionMixin):

    caid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, index=True, nullable=False)
    title = db.Column(db.String(50), unique=True, index=True, nullable=False)

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return '<Category: %r>' % self.name


class Tag(db.Model, SessionMixin):

    tid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, index=True, nullable=False)
    title = db.Column(db.String(50), unique=True, index=True, nullable=False)

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return '<Tag: %r>' % self.name


class Article(db.Model, SessionMixin):

    __searchable__ = ['title', 'content']

    aid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, index=True, nullable=False)
    content = db.Column(db.Text)
    status = db.Column(db.Integer, default=1)  # 0, 草稿、1, 完成、-1,  失效
    created_time = db.Column(db.DateTime, default=datetime.now)
    modified_time = db.Column(db.DateTime, default=datetime.now)
    is_always_above = db.Column(db.Integer, default=0)  # 置顶 0,1
    share = db.Column(db.Integer, default=0)  # 分享到社交网络
    click_count = db.Column(db.Integer, default=0)
    category_id = db.Column(db.Integer, db.ForeignKey('category.caid'))
    category = db.relationship('Category', backref=db.backref('articles', lazy='dynamic'), lazy='select')
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), default=1)
    author = db.relationship('User', backref='articles', lazy='select')
    tags = db.relationship('Tag', secondary=article_tags, backref=db.backref('articles', lazy='dynamic'))

    def __unicode__(self):
        return self.title

    def __repr__(self):
        return '<Article: %r, posted on %r>' % (self.title, self.modified_time)

    def article_abstract(self):
        return re.split(r'<!--more-->', self.content)[0]

    def inc_click(self):
        self.click_count += 1
        db.session.commit()


class Comment(db.Model, SessionMixin):

    coid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    email_address = db.Column(db.String(80))
    site = db.Column(db.String(100))
    avatar = db.Column(db.String(100))  # 头像
    content = db.Column(db.Text)
    post_date = db.Column(db.DateTime, default=datetime.now)
    visible = db.Column(db.Integer, default=1)  # 是否展示
    ip = db.Column(db.String(15))
    reply_to_comment_id = db.Column(db.Integer, db.ForeignKey('comment.coid'))
    reply_to_comment = db.relationship('Comment', backref='comments', remote_side=[coid])
    article_id = db.Column(db.Integer, db.ForeignKey('article.aid'))
    article = db.relationship('Article', backref=db.backref('comments', lazy='dynamic'))

    def __unicode__(self):
        return self.content

    def __repr__(self):
        return '<Comment: #%r, posted on %r>' % (self.coid, self.post_date)


class User(db.Model, SessionMixin):

    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.BigInteger)
    name = db.Column(db.String(50), unique=True, nullable=False, index=True)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)

    role = db.Column(db.String(10), default='admin')
    active = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    created = db.Column(db.DateTime, default=datetime.utcnow)
    avatar = db.Column(db.String(100))
    token = db.Column(db.String(20))
    login_type = db.Column(db.Integer)  # 1:weibo; 2: uid;

    def __init__(self, **kwargs):
        self.token = self.create_token(16)

        if 'username' in kwargs:
            username = kwargs.pop('username')
            self.name = username.lower()

        if 'password' in kwargs:
            rawpass = kwargs.pop('password')
            self.password = self.create_password(rawpass)

        if 'email' in kwargs:
            email = kwargs.pop('email')
            self.email = email.lower()

        for k, v in kwargs.items():
            setattr(self, k, v)

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return '<User: %r at  %r>' % (self.name, self.email)

    @staticmethod
    def create_password(rawpass):
        passwd = '%s%s' % (rawpass, db.app.config['PASSWORD_SECRET'])
        return security.generate_password_hash(passwd)

    @staticmethod
    def create_token(length=16):
        return security.gen_salt(length)

    @property
    def is_admin(self):
        if self.role == 'admin':
            return True

    def check_password(self, rawpass):
        passwd = '%s%s' % (rawpass, db.app.config['PASSWORD_SECRET'])
        return security.check_password_hash(self.password, passwd)

    def change_password(self, rawpass):
        self.password = self.create_password(rawpass)
        self.token = self.create_token()
        return self


class Link(db.Model, SessionMixin):

    lid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    site = db.Column(db.String(100))  # url

    def __unicode__(self):
        return self.name


class BlackList(db.Model, SessionMixin):

    blid = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(15))

    def __unicode__(self):
        return self.ip_address


class Subscriber(db.Model, SessionMixin):

    sid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    email_address = db.Column(db.String(80))
    subscrible_time = db.Column(db.DateTime, default=datetime.now)
    enabled = db.Column(db.Integer, default=True)

    def __unicode__(self):
        return self.username
