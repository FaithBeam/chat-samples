import configparser
import logging

from chatcommands.chatcommand import ChatCommand


class Multiplier(ChatCommand):
    """
    !multiplier
    !multiplier <integer>

    If no integer is supplied, return the multiplier. If an integer is supplied, set the multiplier to the integer.
    """
    def __init__(self, multipy_amt, c, channel):
        super().__init__(c, channel)
        self.multipy_amt = multipy_amt
        self.do_work()

    def do_work(self):
        config = configparser.ConfigParser()
        config.read("./config/config.ini")
        if int(self.multipy_amt) < 1:
            msg = f"Multiplier is {config['SLOTS']['MULTIPLIER']}."
            logging.info(msg)
            self.send_message(msg)
            return
        config.set("SLOTS", "MULTIPLIER", self.multipy_amt)
        with open("./config/config.ini", 'w') as configfile:
            config.write(configfile)
        msg = f"Set multiplier to {self.multipy_amt}."
        logging.info(msg)
        self.send_message(msg)
