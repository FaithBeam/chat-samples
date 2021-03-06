import logging

from chatcommands.chatcommand import ChatCommand
from quotes import Quotes


class DelQuote(ChatCommand):
    """
    !delquote <quote_index>
    Deletes a quote by the index given. Quotes start at 1, not 0.
    """
    def __init__(self, quote_num, c, channel):
        super().__init__(c, channel)
        self.quote_num = quote_num
        self.do_work()

    def do_work(self):
        msg = Quotes().delete_quote(self.quote_num)
        logging.info(msg)
        self.send_message(msg)
