import logging

from config import config
from models.models import Score, ScoreSchema
from template import Template


class CheckUserExists:
    """
    Checks if a user exists within the scores db. If they don't exist,
    create an account for them.
    """

    def __init__(self, user: str):
        self.user = user
        self.do_work()

    def do_work(self):
        my_users = Template(Score, ScoreSchema, ("username", "score"))

        if not my_users.item_exists(self.user):
            my_users.add_item(self.user, int(config["DEFAULT"]["STARTING_CURRENCY"]))
            logging.info(f"{self.user} doesn't exist. Creating user.")
