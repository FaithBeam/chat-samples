import logging

from chatcommands.chatcommand import ChatCommand
from models.models import Score, ScoreSchema
from template import Template


class Scores(ChatCommand):
    """
    !{currency_name}

    Returns the currency amount of the user.
    """

    def __init__(self, user: str, c, channel):
        super().__init__(c, channel)
        self.user = user
        self.do_work()

    def do_work(self):
        msg = Template(Score, ScoreSchema, ("username", "score")).get_value(self.user)
        logging.info(msg)
        self.send_message(str(msg))
