# -*- coding: utf-8 -*-
r"""
    account
    ~~~~~~~

    :copyright: (c) 2013 by Harvey Wang.
"""

from flask import Blueprint
from flask import request, abort, g
from flask import render_template, url_for, redirect
from flask import jsonify
from ..models import Article, Category, Tag
from ..utils.data_wrapper import *
from ..utils.snippets import paginator_obj, timer_function
from .._settings import PAGE_SIZE
from ..forms import CommentForm

__all__ = ['bp']

per_page = PAGE_SIZE

bp = Blueprint('blog', __name__)


@bp.route('/', methods=['GET'])
@bp.route('/index', methods=['GET'])
@bp.route('/page/<int:page>', methods=['GET'])
def index(page=1):
    pagination = get_articles_by_page(page, per_page)
    articles = pagination.items
    categories = timer_function(fetch_all_categories, opname="categories")
    paginator = paginator_obj(pagination)

    return render_template(
        'dopetrope/index.html',
        nav_current='index',
        url='/page/',
        categories=categories,
        articles=articles,
        paginator=paginator,
    )


@bp.route('/article/<int:aid>')
def article(aid):
    try:
        article = Article.query.get(aid)
        article.inc_click()
        print "Page click count of article %s is %d" % \
            (article.title, article.click_count)
        comments_count = get_comments_nums(article_id=aid)
        top_comments = get_top_comments(article.aid)

        form = CommentForm()

        return render_template(
            'dopetrope/article/article.html',
            nav_current='index',
            article=article,
            article_id=aid,
            comments_count=comments_count,
            top_comments=top_comments,
            is_contact=False,
            form=form
        )

    except:
        abort(404)


@bp.route('/comment', methods=['GET', 'POST'])
@bp.route('/comment/<int:article_id>', methods=['GET', 'POST'])
def comment(article_id=0):
    if request.method == 'POST':
        article = Article.query.filter_by(aid=article_id).first()
        inserted_id = comment_insertion(request, article_id=article_id)
        comments_count = get_comments_nums(article_id=article_id)
        top_comments = get_top_comments(article_id=article_id)

        # TODO: Here gose some condition checkings
        status = 0
        comments = None

        if status == 0:
            send_comment_notification(request, article_id)

            if not article_id == 0:
                comments = render_template(
                    'dopetrope/comment/comments.html',
                    is_contact=False,
                    article=article,
                    article_id=article_id,
                    comments_count=comments_count,
                    top_comments=top_comments)
            else:
                comments = render_template(
                    'dopetrope/comment/comments.html',
                    is_contact=True,
                    article_id=0,
                    comments_count=comments_count,
                    top_comments=top_comments)

        rv = jsonify(
            status=status,
            comments=comments,
            inserted_id=inserted_id
        )

        return rv


@bp.route('/categories')
def categories():
    return render_template(
        'dopetrope/category/categories.html',
        title=u'所有分类',
        nav_current='category'
    )

    abort(404)


@bp.route('/category/<name>')
@bp.route('/category/<name>/<int:page>')
def category(name, page=1):
    category = Category.query.filter_by(name=name).first()
    pagination = Article.query.filter_by(category_id=category.caid).paginate(page, per_page)
    articles = pagination.items
    paginator = paginator_obj(pagination)

    return render_template(
        'dopetrope/category/category.html',
        title=u'博客分类%s' % category.title,
        url='/category/%s/' % category.name,
        nav_current='category',
        category=category,
        articles=articles,
        paginator=paginator,
    )

    abort(404)


@bp.route('/tag/<name>')
@bp.route('/tag/<name>/<int:page>')
def tag(name, page=1):
    tag = Tag.query.filter_by(name=name).first()
    pagination = tag.articles.paginate(page, per_page)
    articles = pagination.items
    paginator = paginator_obj(pagination)

    return render_template(
        'dopetrope/tag/tag.html',
        title=u'标签%s' % tag.title,
        url='/tag/%s/' % tag.name,
        tag=tag,
        articles=articles,
        paginator=paginator,
    )

    abort(404)


@bp.route('/contact')
def contact():
    comments_count = get_comments_nums(article_id=0)
    print 'contact account = %d' % comments_count
    top_comments = get_top_comments(article_id=0)
    print 'top comments on contact page are: %s' % top_comments
    form = CommentForm()

    return render_template(
        'dopetrope/contact/contact.html',
        nav_current='contact',
        is_contact=True,
        article_id=0,
        comments_count=comments_count,
        top_comments=top_comments,
        form=form
    )

    abort(404)


@bp.route('/about')
def about():
    return render_template(
        'dopetrope/about/about.html',
        title=u"关于博主",
        nav_current="about"
    )

    abort(404)


@bp.route('/search', methods=['POST'])
def search():
    if not g.search_form.validate_on_submit():
        return redirect(url_for('index'))
    return redirect(url_for('blog.search_results', query=g.search_form.search.data))


@bp.route('/search_results/<query>')
@bp.route('/search_results/<query>/<int:page>')
def search_results(query, page=1):
    articles = Article.query.whoosh_search(query).all()
    count = len(articles)

    return render_template(
        'dopetrope/search/search.html',
        title=u'搜索%s' % query,
        count=count,
        url='/search_results/%s/' % query,
        articles=articles,
    )


@bp.route('/rss')
def rss():
    return "rss"
