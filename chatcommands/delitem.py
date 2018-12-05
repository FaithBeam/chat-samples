import logging

from chatcommands.chatcommand import ChatCommand
from template import Template


class DelItem(ChatCommand):
    def __init__(self, item, c, channel):
        super().__init__(c, channel)
        self.item = item
        self.do_work()

    def do_work(self):
        msg = Template("shop", ("Item Name", "Price")).delete_item(self.item)
        logging.info(msg)
        self.send_message(msg)
