"""
Provides a way to limit how often a user's command is acknowledged by the
bot. The username is used as a key in the dictionary and the value is the
time when that user is allowed to do another command. The set time is created
by getting the current time and adding the delay to it.
"""
import datetime


class Timeouts:
    def __init__(self):
        self.users = {}

    def user_can_message(self, username: str, sec_delay, set_time=True) -> bool:
        """
        Return if a user can send a command to the bot. Check if the current
        time is greater than the stored time plus message delay to determine
        if the user can command.

        :param sec_delay:
        :param username:
        :return: True or false
        """
        now = datetime.datetime.now()
        if username in self.users:
            if now > self.users[username]:
                if set_time:
                    self.users[username] = now + datetime.timedelta(seconds=sec_delay)
                return True
            else:
                return False
        else:
            if set_time:
                self.users[username] = now + datetime.timedelta(seconds=sec_delay)
            return True
