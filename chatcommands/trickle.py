import logging

from chatcommands.chatcommand import ChatCommand
from config import config, config_file


class Trickle(ChatCommand):
    """
    !trickle
    !trickle <integer>

    If no integer is supplied, return the current trickle amount. If an
    integer is supplied, set the trickle amount to the integer.
    """

    def __init__(self, trickle_amt, c, channel):
        super().__init__(c, channel)
        self.trickle_amt = trickle_amt
        self.do_work()

    def do_work(self):
        if int(self.trickle_amt) < 1:
            msg = f"Trickle is {config['TRICKLE']['TRICKLE']}."
            logging.info(msg)
            self.send_message(msg)
            return
        config.set("TRICKLE", "TRICKLE", self.trickle_amt)
        with open(config_file, "w") as configfile:
            config.write(configfile)
        msg = f"Set trickle to {self.trickle_amt}."
        logging.info(msg)
        self.send_message(msg)
