import logging

from chatcommands.chatcommand import ChatCommand


class Say(ChatCommand):
    """
    !say <your text here>

    Whisper the bot with the say command to make the bot say the supplied
    message.
    """

    def __init__(self, msg, c, channel):
        super().__init__(c, channel)
        self.msg = msg
        self.do_work()

    def do_work(self):
        logging.info(self.msg)
        self.send_message(self.msg)
