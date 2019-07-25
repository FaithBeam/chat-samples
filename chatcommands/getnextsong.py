import logging
import queue

from chatcommands.chatcommand import ChatCommand


class GetNextSong(ChatCommand):
    """
    Returns the next song in the songqueue.
    """

    def __init__(self, music_queue: queue, c, channel):
        super().__init__(c, channel)
        self.music_queue = music_queue
        self.do_work()

    def do_work(self):
        if len(self.music_queue.queue) > 0:
            yt_link = self.music_queue.get()
            msg = (
                f"{yt_link}\t There are {len(self.music_queue.queue)} "
                f"songs left in the queue."
            )
            logging.info(msg)
            self.send_message(msg)
        else:
            msg = "No more songs in the queue."
            logging.info(msg)
            self.send_message(msg)
