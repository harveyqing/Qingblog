# -*- coding: utf-8 -*-
r"""
    data_wrapper
    ~~~~~~~

    Wrapper for models handling.

    :copyright: (c) 2013 by Harvey Wang.
"""

import hashlib
import urllib2
from datetime import datetime
from sqlalchemy import desc
from flask import render_template
from ..models import Category, Article, Comment, Link, Tag, User, db
from .snippets import *

__all__ = [
    'fetch_all_categories', 'fetch_all_links',
    'fetch_all_tags', 'fetch_admin',
    'fetch_hotest_articles', 'fetch_category_articles',
    'get_articles_by_page', 'get_connection',
    'get_comments_nums', 'get_top_comments',
    'get_article_comments', 'get_recent_comments',
    'comment_insertion', 'send_comment_notification']

fetch_all_categories = lambda: Category.query.all()
fetch_all_links = lambda: Link.query.all()
fetch_all_tags = lambda: Tag.query.all()
fetch_admin = lambda: User.query.filter_by(id=1).first()
fetch_hotest_articles = lambda: Article.query.order_by(desc(Article.click_count)).limit(5).all()
fetch_category_articles = lambda category, limitation: \
    Article.query.filter_by(category_id=category).order_by(desc('aid')).limit(limitation).all()

    # Article.query.filter_by(Article.category_id=category).order_by(desc('aid')).limit(limitation).all()


def get_articles_by_page(pid, per_page):
    pg = Article.query.order_by(Article.created_time.desc()).paginate(pid, per_page)
    return pg


def get_connection():
    engine = db.get_engine(db.app)
    conn = engine.connect()

    return conn


def get_comments_nums(article_id=None, contact=None):
    if article_id is not None:
        query = """SELECT COUNT(*) FROM comment WHERE article_id=%d""" % int(article_id)

        rv = db.connection.execute(query).first()[0]
        return rv
    else:
        return None


def get_top_comments(article_id=0):
    top_query = """SELECT * FROM comment WHERE article_id=%d
                            AND visible=1 AND reply_to_comment_id=0
                            ORDER BY post_date ASC """ % int(article_id)
    qrs = db.connection.execute(top_query).fetchall()

    return qrs


def get_article_comments(article_id, qr):
    entries = []
    last_qr = qr
    while True:
        try:
            entry_query = """SELECT * FROM comment WHERE article_id=%d
                                    AND visible=1 AND reply_to_comment_id=%d
                                    ORDER BY coid ASC """ % (int(article_id), int(last_qr[0]))
            last_qr = db.connection.execute(entry_query).fetchone()
            if not last_qr:
                break
            entries.append(last_qr)
        except:
            break

    return entries

get_recent_comments = lambda limitation=5: \
    Comment.query.filter(Comment.article_id != 0).order_by(desc('post_date')).limit(limitation).all()


def comment_insertion(request, article_id=None):
    username = request.form['username']
    reply_to_comment_id = request.form['reply_to_comment']
    site = request.form['site']
    content = request.form['content']
    avatar = request.form['avatar']
    email = request.form['email']
    ip = get_remote_ip()

    reply_to_comment_id = reply_to_comment_id and reply_to_comment_id or 0
    content = escape_comment(content)
    post_date = datetime.now()

    if not avatar or len(avatar.strip()) == 0:
        email_hash = hashlib.md5(email.strip()).hexdigest()
        try:
            avatar_url = 'http://www.gravatar.com/avatar/%s?s=40&d=404' % email_hash
            urllib2.urlopen(avatar_url)
            avatar = avatar_url
        except urllib2.URLError:
            avatar = ''

    # Comment an article, not leave a message
    article_id = article_id and article_id or 0
    insert_query = """INSERT INTO comment (username, email_address, site, avatar,
                                content, post_date, visible, ip, reply_to_comment_id, article_id)
                                VALUES ("%s", "%s", "%s", "%s", "%s", "%s","%d", "%s", "%s", "%s")""" % \
                                (username, email, site, avatar, content, post_date, 1, ip, reply_to_comment_id, article_id)
    try:
        rslt = db.connection.execute(insert_query)
        return rslt.lastrowid
    except:
        pass


def send_comment_notification(request, article_id=0):
    from ..utils.mail import send_email
    from .._settings import ADMINS, SITE_TITLE, BLOGGER

    reply_username = request.form['username']
    replied_comment_id = request.form['reply_to_comment'] \
        and request.form['reply_to_comment'] \
        or 0
    # print u'回复的评论id为%s' % replied_comment_id
    replied_username = replied_comment_id == 0 and BLOGGER \
        or Comment.query.get(replied_comment_id).username
    replied_email = replied_comment_id == 0 and ADMINS[0] \
        or Comment.query.get(replied_comment_id).email_address
    # print u'回复的用户名为%s，邮箱地址为%s' % (replied_username, replied_email)
    is_contact = article_id == 0 and True or False
    article = is_contact is False and Article.query.get(article_id) or None

    sender = ADMINS[0]

    send_email(
        u'【您在%s有新动态】' % SITE_TITLE,
        sender,
        [replied_email],
        render_template(
            'dopetrope/email/comment_notification.txt',
            replied_username=replied_username,
            reply_username=reply_username,
            replied_comment_id=replied_comment_id,
            site_title=SITE_TITLE,
            is_contact=is_contact,
            article=article),
        render_template(
            'dopetrope/email/comment_notification.html',
            replied_username=replied_username,
            reply_username=reply_username,
            replied_comment_id=replied_comment_id,
            site_title=SITE_TITLE,
            is_contact=is_contact,
            article=article)
    )

