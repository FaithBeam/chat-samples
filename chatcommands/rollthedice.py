import logging
import random

from chatcommands.chatcommand import ChatCommand
from config import config


class RollTheDice(ChatCommand):
    """
    !roll

    Rolls a die.
    """
    def __init__(self, user: str, c, channel):
        super().__init__(c, channel)
        self.user = user
        self.do_work()

    def do_work(self):
        dice_game_enabled = config["DICE"]["DICE_ENABLED"]

        if dice_game_enabled == "true":
            max_roll = config["DICE"]["MAX_ROLL"]
            rand_num = random.randint(0, int(max_roll))

            msg = f"{self.user} rolled: {str(rand_num)}."
            logging.info(msg)
            self.send_message(msg)
