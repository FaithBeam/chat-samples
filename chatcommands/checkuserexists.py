import logging

from config import config
from template import Template


class CheckUserExists:
    def __init__(
            self,
            user: str
    ):
        self.user = user
        self.do_work()

    def do_work(self):
        my_users = Template("scores", ("Username", "Score"))

        if not my_users.item_exists(self.user):
            my_users.add_item(self.user, int(config["DEFAULT"]["STARTING_CURRENCY"]))
            logging.info(f"{self.user} doesn't exist. Creating user.")
