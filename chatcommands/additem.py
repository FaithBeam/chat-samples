import logging

from chatcommands.chatcommand import ChatCommand
from models.models import Shop, ShopSchema
from template import Template


class AddItem(ChatCommand):
    """
    !additem <item_name> <price>
    Add an item to the shop db.
    """

    def __init__(self, item, val, c, channel):
        super().__init__(c, channel)
        self.item = item
        self.val = val
        self.do_work()

    def do_work(self):
        msg = Template(Shop, ShopSchema, ("item_name", "price")).add_item(
            self.item, self.val
        )
        logging.info(msg)
        self.send_message(msg)
