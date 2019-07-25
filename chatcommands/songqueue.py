import logging

from chatcommands.chatcommand import ChatCommand


class SongQueue(ChatCommand):
    """
    !songqueue

    Lists the songs in the songqueue with who requested it and their position.
    """

    def __init__(self, music_queue, c, channel):
        super().__init__(c, channel)
        self.music_queue = music_queue
        self.do_work()

    def do_work(self):
        if len(self.music_queue.queue) > 0:
            msg = ""
            for i in range(len(self.music_queue.queue)):
                msg = f", #{i+1}: ".join([msg, self.music_queue.queue[i]])
                msg = msg[2:]
                logging.info(msg)
                self.send_message(msg)
        else:
            msg = "No songs in the queue."
            logging.info(msg)
            self.send_message(msg)
