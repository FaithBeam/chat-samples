import logging

from chatcommands.chatcommand import ChatCommand
from models.models import Shop, ShopSchema
from db_connection_utilities import DbConnectionUtilities


class DelItem(ChatCommand):
    """
    !delitem <shop_item_name>
    Deletes an item from the shop.
    """

    def __init__(self, item, c, channel):
        super().__init__(c, channel)
        self.item = item
        self.do_work()

    def do_work(self):
        msg = DbConnectionUtilities(Shop, ShopSchema, ("item_name", "price")).delete_item(self.item)
        logging.info(msg)
        self.send_message(msg)
