import logging


class ChatCommand:
    """
    Parent class that should be inherited from to create a new command.
    """

    def __init__(self, c, channel):
        self.c = c
        self.channel = channel

    def send_message(self, msg: str):
        self.c.privmsg(self.channel, msg)

    def send_whisper(self, msg: str, user: str):
        msg = " ".join(["/w", user, msg])
        logging.info(msg)
        self.c.privmsg(self.channel, msg)
