import logging

from chatcommands.chatcommand import ChatCommand
from quotes import Quotes


class AddQuote(ChatCommand):
    """
    !addquote <your quote here>
    Add a quote to the quote db.
    """
    def __init__(self, quote, c, channel):
        super().__init__(c, channel)
        self.quote = quote
        self.do_work()

    def do_work(self):
        msg = Quotes().add_quote(self.quote)
        logging.info(msg)
        self.send_message(msg)
