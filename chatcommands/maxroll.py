import logging

from chatcommands.chatcommand import ChatCommand
from config import config, config_file


class MaxRoll(ChatCommand):
    """
    !maxroll
    !maxroll <integer>

    If no integer is supplied, return the current highest allowed roll. If an
    integer is supplied, change the max roll to that integer.
    """

    def __init__(self, max_roll: str, c, channel):
        super().__init__(c, channel)
        self.max_roll = max_roll
        self.do_work()

    def do_work(self):
        if self.max_roll == -1:
            msg = f"Max roll is: {config['DICE']['MAX_ROLL']}"
            logging.info(msg)
            self.send_message(msg)
        elif self.max_roll.isdigit():
            config.set("DICE", "MAX_ROLL", self.max_roll)
            with open(config_file, "w") as configfile:
                config.write(configfile)
            msg = f"Set max roll to: {self.max_roll}."
            logging.info(msg)
            self.send_message(msg)
        else:
            msg = f"No."
            logging.info(msg)
            self.send_message(msg)
