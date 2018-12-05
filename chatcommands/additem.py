import logging

from chatcommands.chatcommand import ChatCommand
from template import Template


class AddItem(ChatCommand):
    def __init__(self, item, val, c, channel):
        super().__init__(c, channel)
        self.item = item
        self.val = val
        self.do_work()

    def do_work(self):
        msg = Template("shop", ("Item Name", "Price")).add_item(self.item,
                                                                self.val)
        logging.info(msg)
        self.send_message(msg)
