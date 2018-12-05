import datetime
from unittest import TestCase

from timeouts import Timeouts


class TestAuthentication(TestCase):
    def test_user_can_message(self):
        assert self.test_auth.user_can_message(self.test_usr, 120) is True

        assert self.test_auth.user_can_message(self.test_usr, 120) is False

        now = datetime.datetime(
            year=9999, month=1, day=1, hour=1, minute=1, second=1
        )
        self.test_auth.users = {self.test_usr: now}
        assert self.test_auth.user_can_message(self.test_usr, 120) is False

        now = datetime.datetime(
            year=500, month=1, day=1, hour=1, minute=1, second=1
        )
        self.test_auth.users = {self.test_usr: now}
        assert self.test_auth.user_can_message(self.test_usr, 120) is True

    def test__set_time(self):
        now = datetime.datetime(
            year=9999, month=1, day=1, hour=1, minute=1, second=1
        )
        self.test_auth._set_time(self.test_usr, now, 4)
        now = datetime.datetime(
            year=9999, month=1, day=1, hour=1, minute=1, second=5
        )
        assert self.test_auth.users[self.test_usr] == now

    def test__user_exists(self):
        assert self.test_auth._user_exists(self.test_usr) is False

        self.test_auth.users = {self.test_usr: 'jdhfg'}
        assert self.test_auth._user_exists(self.test_usr) is True

    def setUp(self):
        self.test_usr = 'test-username'
        self.test_auth = Timeouts()

    def tearDown(self):
        del self.test_auth
