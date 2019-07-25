import logging

from chatcommands.chatcommand import ChatCommand
from commands import Commands


class CheckCustomCommands(ChatCommand):
    """
    Returns true or false if a custom command exists in the db.
    """

    def __init__(self, command, c, channel):
        super().__init__(c, channel)
        self.command = command

    def do_work(self):
        msg = Commands().item_exists(self.command)
        logging.info(msg)
        return msg
