# -*- coding: utf-8 -*-

import time
from flask import request, escape
from .._settings import PAGE_ENTRY_DISPLAY_NUM, PAGE_ENTRY_EDGE_NUM

__all__ = [
    'Timer', 'timer_function',
    'paginator_obj', 'get_remote_ip',
    'escape_comment']


class Timer(object):
    """A simple profiler."""

    def __init__(self, verbose=False):
        self.verbose = verbose

    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, *args):
        self.end = time.time()
        self.secs = self.end - self.start
        self.msecs = self.secs * 1000
        if self.verbose:
            print 'elapsed time: %f ms' % self.msecs


def timer_function(func, opname=None, *args, **kwargs):
    with Timer() as t:
        rv = func(*args, **kwargs)
    print "=> Query %s, elapsed: %s" % (opname, t.secs)

    if rv:
        return rv


def paginator_obj(page_obj):
    page = int(page_obj.page)
    pages = int(page_obj.pages)

    left_continual_max = PAGE_ENTRY_EDGE_NUM + PAGE_ENTRY_DISPLAY_NUM / 2 + 1
    left_edge_range = range(1, PAGE_ENTRY_EDGE_NUM + 1)
    left_continual_range = range(1, page)
    left_range = range(page - PAGE_ENTRY_DISPLAY_NUM / 2, page)

    right_continual_min = pages - \
        PAGE_ENTRY_DISPLAY_NUM / 2 - 1 \
            if PAGE_ENTRY_DISPLAY_NUM % 2 == 0 \
            else PAGE_ENTRY_DISPLAY_NUM / 2
    right_continual_range = range(page + 1, pages + 1)
    right_edge_range = range(pages - PAGE_ENTRY_EDGE_NUM + 1, pages + 1)
    right_range = range(page + 1, page + PAGE_ENTRY_EDGE_NUM + 1)

    pagination = page_obj

    vars = locals()
    del vars['pages']
    return vars


def get_remote_ip():
    return request.remote_addr

escape_comment = lambda content: escape(content).replace('\n', '<br />')
