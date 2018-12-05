import logging

from chatcommands.chatcommand import ChatCommand
from template import Template


class Winners(ChatCommand):
    def __init__(self, c, channel):
        super().__init__(c, channel)
        self.do_work()

    def do_work(self):
        my_users = Template("scores", ("Username", "Score"))
        msg = my_users.get_top("Score")
        logging.info(msg)
        self.send_message(msg)
