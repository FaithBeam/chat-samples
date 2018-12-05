"""
Provides a way to limit how often a user's command is acknowledged by the
bot. The username is used as a key in the dictionary and the value is the
time when that user is allowed to do another command. The set time is created by
getting the current time and adding the delay to it.
"""
import datetime


class Timeouts:
    def __init__(self):
        self.users = {}

    def user_can_message(
            self,
            username: str,
            sec_delay,
            set_time=True
    ) -> bool:
        """
        Return if a user can send a command to the bot. Check if the current
        time is greater than the stored time plus message delay to determine
        if the user can command.

        :param sec_delay:
        :param username:
        :return: True or false
        """
        now = datetime.datetime.now()
        if self._user_exists(username):
            if now > self.users[username]:
                if set_time:
                    self._set_time(username, now, sec_delay)
                return True
            else:
                return False
        else:
            if set_time:
                self._set_time(username, now, sec_delay)
            return True

    def _set_time(
            self,
            username: str,
            time: datetime.datetime,
            sec_delay: int
    ):
        """Sets when a user's commands are acknowledged again. After time +
        delay."""
        self.users[username] = \
            time + datetime.timedelta(seconds=sec_delay)

    def _user_exists(
            self,
            username: str
    ) -> bool:
        """Return true of false if a user has already sent a command."""
        return username in self.users
