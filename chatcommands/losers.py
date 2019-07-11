import logging

from chatcommands.chatcommand import ChatCommand
from models.models import Score, ScoreSchema
from template import Template


class Losers(ChatCommand):
    """
    !losers
    Returns the three users with the lowest currency.
    """
    def __init__(self, c, channel):
        super().__init__(c, channel)
        self.do_work()

    def do_work(self):
        my_users = Template(Score, ScoreSchema, ("username", "score"))
        msg = my_users.get_bottom("Score")
        logging.info(msg)
        self.send_message(msg)
