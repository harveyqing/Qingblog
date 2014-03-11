# -*- coding: utf-8 -*-
"""Base test class for the Qingblog application."""

import os
import tempfile
import unittest
from Qingblog.app import create_app
from Qingblog.models import db


class _BaseCase(unittest.TestCase):
    """Base test case for Qingblog"""

    def setUp(self):
        """Pre-test activities."""
        config = {'TESTING': True}
        config['CSRF_ENABLED'] = False
        config['SECRET_KEY'] = 'secret-key-for-Qingblog-test'
        config['SQLALCHEMY_POOL_SIZE'] = 5

        # Set up a temp-database each test case.
        self.db_fd, self.db_file = tempfile.mkstemp()
        config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s' % self.db_file

        app = create_app(config)
        self.app = app
        self.client = app.test_client()

        # Init the database
        db.create_all()

    def tearDown(self):
        """Get rid of the database again after each test."""
        db.drop_all()

        os.close(self.db_fd)
        #os.unlink(self.db_file)

    # Helper functions
    def create_admin(self):
        pass
