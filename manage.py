# coding: utf-8

import gevent.monkey
gevent.monkey.patch_all()

import os
import sys
from flask.ext.script import Manager
from Qingblog.app import create_app

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(ROOT_DIR, 'data', 'profile.log')

app = create_app()
manager = Manager(app)


@manager.command
def runserver(port=5000, with_profile=True):
    """Runs a development server."""
    from gevent.wsgi import WSGIServer
    from werkzeug.serving import run_with_reloader
    from werkzeug.debug import DebuggedApplication
    from werkzeug.contrib.profiler import ProfilerMiddleware

    port = int(port)

    if with_profile:
        f = open(LOG_FILE, 'w')
        wsgi = ProfilerMiddleware(app, f)
    else:
        wsgi = DebuggedApplication(app)

    @run_with_reloader
    def run_server():
        print('start server at: 127.0.0.1:%s' % port)

        http_server = WSGIServer(('', port), wsgi)
        http_server.serve_forever()

    try:
        run_server()
    except (KeyboardInterrupt, TypeError):
        sys.exit()


@manager.command
def createdb():
    """Create a database and init the administrator account."""
    from Qingblog.models import db
    db.create_all()

    from Qingblog.models import User 
    admin = User(id=1, name='harvey', password='123456',
    email='harveyqing@gmail.com', role='admin')
    db.session.add(admin)
    db.session.commit()

if __name__ == '__main__':
    manager.run()
