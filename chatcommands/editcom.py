import logging

from chatcommands.chatcommand import ChatCommand
from commands import Commands


class EditCom(ChatCommand):
    def __init__(self, command, val, c, channel):
        super().__init__(c, channel)
        self.command = command
        self.val = val
        self.do_work()

    def do_work(self):
        msg = Commands().set_value(self.command, self.val)
        logging.info(msg)
        self.send_message(msg)
