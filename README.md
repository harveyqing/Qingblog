Qingblog - A Flask based personal blog.
=======================================

A personal web blog based on the Python Flask Web Framework.

Features:
======

- Support code highlighting in your articles (via using `Syntax Highlighting`)

- Multi-Browser Support UI (tested on most popular browsers)

- Tags & Categories, so you can manage your posts easily

- Storing comments & messages locally, so you can backup yourselves

- Support a full text search

- E-mail notification for comments

- With a administrative pannel, where you can manage your data

- With a realtime preview markdown editor so you can write articles with a markdown format

...
and you can explore yourselves if you want (^ ^)

Notes:
======

- The current version is setup to use sqlite. Just makes it easier to test.

- If you want to use it smoothly, you may change some settings in `Qingblog._settings.py`.


To setup locally:
======
Run:

    python virtualenv.py Qingblog

Then install requirements:

    Qingblog/bin/pip install -r Qingblog/Qingblog/requirements.txt

* Note: I just list a part of required libraries in the `requirements.txt` file, others can be installed themselves while they are needed.

Init the database and set a `admin` user:
   python manage.py createdb

* Note: The initial `admin` account use `name=harvey`, `password=123456`, `email=harveyqing@gmail.com`, you can change in the `manage.py`.

Start server:

    python manage.py runserver

Now just open your browser and type:
    
    localhost:5000

in the address bar

You may want to know:
======
- how can I login as the administrator:
    your_host/account/signin

- how can I enter the backstage:
    your_host/Qingblog/admin

- how can I use the markdown editor:
    your_host/edit/editor
