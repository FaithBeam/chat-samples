import logging

from chatcommands.chatcommand import ChatCommand
from config import config, config_file


class DiceGame(ChatCommand):
    """
    !dicegame
    Flips the !roll command on or off. If the game is turned on, turn it off, and if the game is off, turn it on.
    """
    def __init__(self, c, channel):
        super().__init__(c, channel)
        self.do_work()

    def do_work(self):
        dice_game_enabled = config["DICE"]["DICE_ENABLED"]

        if dice_game_enabled == "true":
            config.set("DICE", "DICE_ENABLED", "false")
            msg = "Disabled dice."
        elif dice_game_enabled == "false":
            config.set("DICE", "DICE_ENABLED", "true")
            msg = "Enabled dice."
        else:
            msg = "Enabled dice."
            config.set("DICE", "DICE_ENABLED", "true")
        with open(config_file, 'w') as configfile:
            config.write(configfile)

        logging.info(msg)
        self.send_message(msg)
