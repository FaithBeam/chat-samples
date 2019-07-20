import logging

from chatcommands.chatcommand import ChatCommand
from models.models import Shop, ShopSchema
from template import Template
import models.models


class Shop(ChatCommand):
    """
    !shop

    Returns a list of items in the shop with their price.
    """
    def __init__(self, c, channel):
        super().__init__(c, channel)
        self.do_work()

    def do_work(self):
        msg = Template(models.models.Shop, models.models.ShopSchema,
                       ("item_name", "price"))\
            .get_items_descending("price", 999)
        logging.info(msg)
        self.send_message(msg)
