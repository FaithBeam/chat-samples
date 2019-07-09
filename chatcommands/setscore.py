import logging

from chatcommands.chatcommand import ChatCommand
from models.models import Score, ScoreSchema
from template import Template


class SetScore(ChatCommand):
    """
    !setscore <user> <integer>

    Sets the user's currency to the amount.
    """
    def __init__(self, user: str, score: str, c, channel):
        super().__init__(c, channel)
        self.user = user
        self.score = score
        self.do_work()

    def do_work(self):
        my_users = Template(Score, ScoreSchema, ("Username", "Score"))

        if self.score.isdigit():
            msg = my_users.set_value(self.user, int(self.score))
            logging.info(msg)
            self.send_message(msg)
            return
        msg = "No."
        logging.info(msg)
        self.send_message(msg)
