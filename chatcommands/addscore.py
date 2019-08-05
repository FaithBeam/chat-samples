import logging

from chatcommands.chatcommand import ChatCommand
from models.models import Score, ScoreSchema
from db_connection_utilities import DbConnectionUtilities


class AddScore(ChatCommand):
    """
    !add{currency_name} <target_user> <amount>
    Add some currency to a user.
    """

    def __init__(self, user: str, score: str, c, channel):
        super().__init__(c, channel)
        self.user = user
        self.score = score
        self.do_work()

    def do_work(self):
        msg = DbConnectionUtilities(Score, ScoreSchema, ("username", "score")).add_to_value(
            self.user, self.score
        )
        logging.info(msg)
        self.send_message(msg)
