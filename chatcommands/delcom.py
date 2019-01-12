import logging

from chatcommands.chatcommand import ChatCommand
from commands import Commands


class DelCom(ChatCommand):
    """
    !delcom <command_name>
    Deletes a command from the custom command db.
    """
    def __init__(self, command, c, channel):
        super().__init__(c, channel)
        self.command = command
        self.do_work()

    def do_work(self):
        msg = Commands().delete_item(self.command)
        logging.info(msg)
        self.send_message(msg)
