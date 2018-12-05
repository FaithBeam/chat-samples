import logging

from chatcommands.chatcommand import ChatCommand
from template import Template
from twitchapi import get_channel_users


class GiveScore(ChatCommand):
    def __init__(self, amount,  c, channel):
        super().__init__(c, channel)
        self.c = c
        self.channel = channel
        self.amount = amount
        self.do_work()

    def do_work(self):
        my_users = Template("scores", ("Username", "Score"))

        if not self.amount.isdigit():
            msg = f"{self.amount} is not valid."
            logging.info(msg)
            return msg
        users = get_channel_users(self.channel[1:])
        for user in users:
            if my_users.item_exists(user):
                my_users.add_to_value(user, self.amount)
        msg = f"Added {self.amount} to everyone in chat."
        logging.info(msg)
        self.send_message(msg)
