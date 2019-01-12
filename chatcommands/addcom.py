import logging

from chatcommands.chatcommand import ChatCommand
from commands import Commands


class AddCom(ChatCommand):
    """
    !addcom <command_name> <strings to return>
    Add a command to the custom commands db.
    """
    def __init__(self, key: str, val: str, c, channel):
        super().__init__(c, channel)
        self.key = key
        self.val = val
        self.do_work()

    def do_work(self):
        msg = Commands().add_item(self.key, self.val)
        logging.info(msg)
        self.send_message(msg)
