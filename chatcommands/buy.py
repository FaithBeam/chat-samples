import logging
import queue

from chatcommands.addsong import AddSong
from chatcommands.chatcommand import ChatCommand
from template import Template


class Buy(ChatCommand):
    def __init__(self, user: str, item: str, music_queue: queue, e, c, channel):
        super().__init__(c, channel)
        self.user = user
        self.item = item
        self.music_queue = music_queue
        self.e = e
        self.do_work()

    def do_work(self):
        my_users = Template("scores", ("Username", "Score"))
        my_shop = Template("shop", ("Item Name", "Price"))

        if not my_users.item_exists(self.user):
            return f"{self.user} doesn't exist."

        if not my_shop.item_exists(self.item):
            return f"{self.item} doesn't exist."

        if not my_users.get_value(self.user) >= my_shop.get_value(self.item):
            msg = (
                f"{self.item} costs {str(my_shop.get_value(self.item))}, "
                f"you have {str(my_users.get_value(self.user))}."
            )
            logging.info(msg)
            self.send_message(msg)
            return

        yt_link = parse_custom_cmd(self.e)
        if yt_link:
            yt_link = yt_link[1]
            if self.item == "songrequest" and yt_link:
                if AddSong(self.user, yt_link, self.music_queue).do_work():
                    msg = f"Added {yt_link} to the queue in position " \
                          f"{len(self.music_queue.queue)}."
                    logging.info(msg)
                    self.send_message(msg)
                else:
                    msg = "Bad YT link."
                    logging.info(msg)
                    self.send_message(msg)
                    return
        else:
            msg = "Need a link."
            logging.info(msg)
            self.send_message(msg)
            return

        my_users.add_to_value(self.user, str(-1 * my_shop.get_value(self.item)))

        msg = (
            f"{self.user} purchased {self.item}. {self.user} has "
            f"{str(my_users.get_value(self.user))}."
        )
        logging.info(msg)
        self.send_message(msg)
        return


def parse_custom_cmd(msg):
    cmd = msg.arguments[0].split(' ', 2)[1:]
    if len(cmd) != 2 or not cmd[0].isalnum():
        return False
    return cmd
