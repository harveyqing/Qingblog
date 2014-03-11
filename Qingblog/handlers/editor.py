# -*- coding: utf-8 -*-
r"""
    account
    ~~~~~~~

    :copyright: (c) 2013 by Harvey Wang.
"""

from flask import Blueprint
from flask import render_template
from ..utils.account import require_admin

__all__ = ['bp']

bp = Blueprint('editor', __name__)


@bp.route('/edit', methods=['GET', 'POST'])
@require_admin
def edit():

    return render_template('editor/editor.html')
