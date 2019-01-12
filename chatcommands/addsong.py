import re


class AddSong:
    """
    Add a song to the songqueue. The link must be a youtube link.
    """
    def __init__(self, user, yt_link: str, music_queue):
        self.user = user
        self.yt_link = yt_link
        self.music_queue = music_queue

    def do_work(self):
        match = re.match(
            '^(https?\:\/\/)?(www\.)?(youtube\.com|youtu\.?be)\/.+$',
            self.yt_link)
        if match:
            self.music_queue.put(": ".join([self.user, self.yt_link]))
            return True
        else:
            return False
