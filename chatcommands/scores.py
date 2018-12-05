import logging

from chatcommands.chatcommand import ChatCommand
from template import Template


class Scores(ChatCommand):
    def __init__(self, user: str, c, channel):
        super().__init__(c, channel)
        self.user = user
        self.do_work()

    def do_work(self):
        msg = Template("scores", ("Username", "Score"))\
            .get_value(self.user)
        logging.info(msg)
        self.send_message(str(msg))
