# -*- coding: utf-8 -*-

from _base import _BaseCase


class SigninTest(_BaseCase):

    def test_get(self):
        rv = self.client.get('/account/signin')

        assert '</form>' in rv.data
