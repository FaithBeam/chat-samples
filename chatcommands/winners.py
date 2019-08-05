import logging

from chatcommands.chatcommand import ChatCommand
from models.models import Score, ScoreSchema
from db_connection_utilities import DbConnectionUtilities


class Winners(ChatCommand):
    """
    !winners

    Returns the three users with the most currency.
    """

    def __init__(self, c, channel):
        super().__init__(c, channel)
        self.do_work()

    def do_work(self):
        my_users = DbConnectionUtilities(Score, ScoreSchema, ("username", "score"))
        msg = my_users.get_top("score")
        logging.info(msg)
        self.send_message(msg)
