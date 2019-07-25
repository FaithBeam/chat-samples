import logging

from chatcommands.chatcommand import ChatCommand
from quotes import Quotes


class EditQuote(ChatCommand):
    """
    !editquote <quote_index> <new quote here>
    Edits an existing quote by index.
    """

    def __init__(self, quote_num, val: str, c, channel):
        super().__init__(c, channel)
        self.quote_num = quote_num
        self.val = val
        self.do_work()

    def do_work(self):
        msg = Quotes().edit_quote(self.quote_num, self.val)
        logging.info(msg)
        self.send_message(msg)
