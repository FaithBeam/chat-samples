import logging

from config import config
from template import Template
from twitchapi import get_channel_users, is_broadcasting


class ScoreTrickle:
    """
    Currency trickle. Everyone in chat with an account in the scores db gets
    1 currency every 600 seconds.
    """
    def __init__(self, channel: str, client_id: str):
        self.channel = channel
        self.client_id = client_id
        self.do_work()

    def do_work(self):
        my_users = Template("scores", ("Username", "Score"))
        trickle = config["TRICKLE"]["TRICKLE"]

        if is_broadcasting(self.channel, self.client_id):
            users = get_channel_users(self.channel)
            msg = "Trickling:"

            for user in users:
                if my_users.item_exists(user):
                    msg = " ".join([msg, user])
                    my_users.add_to_value(user, trickle)
            logging.info(msg)
