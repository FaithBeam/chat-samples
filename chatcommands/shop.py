import logging

from chatcommands.chatcommand import ChatCommand
from template import Template


class Shop(ChatCommand):
    """
    !shop

    Returns a list of items in the shop with their price.
    """
    def __init__(self, c, channel):
        super().__init__(c, channel)
        self.do_work()

    def do_work(self):
        msg = Template("shop", ("Item Name", "Price")).get_items_descending(
            "Price", 999)
        logging.info(msg)
        self.send_message(msg)
