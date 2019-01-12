import logging

from chatcommands.chatcommand import ChatCommand
from commands import Commands


class GetCustomCommands(ChatCommand):
    """
    Returns a list of custom commands from the custom commands db.
    """
    def __init__(self, command, c, channel):
        super().__init__(c, channel)
        self.command = command
        self.do_work()

    def do_work(self):
        msg = Commands().get_value(self.command)
        logging.info(msg)
        self.send_message(msg)
