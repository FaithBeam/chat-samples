import logging

from chatcommands.chatcommand import ChatCommand
from quotes import Quotes


class NumQuotes(ChatCommand):
    """
    !numquotes
    Returns the number of quotes in the quotes db.
    """
    def __init__(self, c, channel):
        super().__init__(c, channel)
        self.do_work()

    def do_work(self):
        msg = Quotes().get_number_quotes()
        logging.info(msg)
        self.send_message(msg)
