# -*- coding: utf-8 -*-

import os
import time
import hashlib
from datetime import datetime

from flask import Flask
from flask import g, request
import flask.ext.whooshalchemy as whooshalchemy
# from flask.ext.babel import gettext as _

from .forms import SearchForm
from .models import db, Article
from .utils.mail import mail
from .utils.constants import month_map


def create_app(config=None):
    app = Flask(
        __name__,
        template_folder='templates')

    app.config.from_pyfile('_settings.py')

    if isinstance(config, dict):
        app.config.update(config)
    elif config:
        app.config.from_pyfile(os.path.abspath(config))

    app.static_folder = app.config.get('STATIC_FOLDER')
    app.config.update({'SITE_TIME': datetime.utcnow()})

    register_hooks(app)
    register_jinja(app)
    register_database(app)
    register_mail(app)
    register_admin(app)
    register_routes(app)
    register_whoosh(app)
    # register_babel(app)

    return app


def register_database(app):
    """Database related configuration."""
    #: prepare for database
    db.init_app(app)
    db.app = app

    from .utils.data_wrapper import get_connection
    db.connection = get_connection()


def register_mail(app):
    mail.init_app(app)
    mail.app = app


def register_hooks(app):
    """Hooks for request."""
    from .utils.account import get_current_user

    #: 每次请求前都尝试获取当前用户
    @app.before_request
    def load_current_user():
        # g.start = time.time()
        g.search_form = SearchForm()
        g.user = get_current_user()
        if g.user:
            g._before_request_time = time.time()

    @app.after_request
    def rendering_time(response):
        # diff = int(time.time() - g.start) * 1000
        # g.render_time = diff

        # if app.debug:
        #     print "Exec time: %s" % str(diff)

        # if (response.response and str(response.content_type).startswith("text/html") and \
        #                                             response.status_code == 200):
        #     response.response[0] = response.response[0].replace('__EXECUTION_TIME__', str(diff))

        if hasattr(g, '_before_request_time'):
            delta = time.time() - g._before_request_time
            response.headers['X-Render-Time'] = delta * 1000

        return response

    @app.teardown_request
    def teardown_request(exception):
        """Closes the database again at the end of the request"""
        pass


def register_routes(app):
    from .handlers import account, blog, editor
    app.register_blueprint(blog.bp, url_prefix='')
    app.register_blueprint(account.bp, url_prefix='/account')
    app.register_blueprint(editor.bp, url_prefix='/editor')

    return app


def register_admin(app):
    from flask.ext.admin import Admin
    from flask.ext.admin.contrib.sqla import ModelView
    from .utils.account import get_current_user
    from .models import (
        Category, Tag,
        Subscriber, Comment,
        User, Link,
        BlackList)

    admin = Admin(app, url='/Qingblog/admin')

    class QingView(ModelView):

        def is_accessible(self):
            return get_current_user()

    admin.add_view(QingView(Tag, db.session))
    admin.add_view(QingView(Category, db.session))
    admin.add_view(QingView(Article, db.session))
    admin.add_view(QingView(Comment, db.session))
    admin.add_view(QingView(User, db.session))
    admin.add_view(QingView(Link, db.session))
    admin.add_view(QingView(BlackList, db.session))
    admin.add_view(QingView(Subscriber, db.session))

    return app


def register_pagedown(app):
    from utils import pagedown

    pagedown.init_app(app)
    pagedown.app = app


def register_jinja(app):
    if not hasattr(app, '_static_hash'):
        app._static_hash = {}

    def static_url(filename):
        if filename in app._static_hash:
            return app._static_hash[filename]

        with open(os.path.join(app.static_folder, filename), 'r') as f:
            content = f.read()
            hsh = hashlib.md5(content).hexdigest()

        prefix = app.config.get('SITE_STATIC_PREFIX', '/static/')
        value = '%s%s?v=%s' % (prefix, filename, hsh[:5])
        app._static_hash[filename] = value
        return value

    def format_posttime(dt):
        return u'%d年%d月%d日 %d:%d %s' % \
            (dt.year, dt.month, dt.day, int(dt.hour), int(dt.minute), dt.hour < 12 and 'a.m.' or 'p.m.')

    def format_commenttime(dt):
        return u'%d-%d-%d %d:%d' % \
            (dt.year, dt.month, dt.day, int(dt.hour), int(dt.minute))

    month_mapping = lambda month: month_map[month]

    app.jinja_env.filters['format_posttime'] = format_posttime
    app.jinja_env.filters['format_commenttime'] = format_commenttime
    app.jinja_env.filters['month_mapping'] = month_mapping

    from .utils.data_wrapper import (
        get_article_comments, fetch_all_links,
        fetch_all_tags, fetch_admin,
        fetch_hotest_articles, fetch_all_categories,
        fetch_category_articles, get_recent_comments)

    @app.context_processor
    def register_context():
        return dict(
            static_url=static_url,
            get_article_comments=get_article_comments,
            fetch_all_categories=fetch_all_categories,
            fetch_all_links=fetch_all_links,
            fetch_all_tags=fetch_all_tags,
            fetch_admin=fetch_admin,
            fetch_hotest_articles=fetch_hotest_articles,
            fetch_category_articles=fetch_category_articles,
            get_recent_comments=get_recent_comments,
        )


def register_whoosh(app):
    whooshalchemy.whoosh_index(app, Article)


# def register_babel(app):
#     from flask.ext.babel import Babel
#     from ._settings import LANGUAGES
# 
#     babel = Babel(app)
# 
#     @babel.localeselector
#     def get_locale():
#         return request.accept_languages.best_match(LANGUAGES.keys())
