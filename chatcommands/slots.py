import logging

from collections import Counter
from random import choice
from chatcommands.chatcommand import ChatCommand
from config import config
from template import Template
from twitchapi import is_vip


logging.getLogger(__name__)


class Slots(ChatCommand):
    """
    !slots

    The slots game. Costs 5 currency to play, but can be played even if you
    don't have enough. In this case you go into negative currency.
    """
    def __init__(self, user: str, c, channel):
        super().__init__(c, channel)
        self.user = user
        self.my_users = Template("scores", ("Username", "Score"))
        self.my_emotes = Template("emotes", ("Emote Name", "Payout Value"))
        self.score = int(self.my_users.get_value(self.user))
        self.score_after = self.score
        self.slot_price = int(config["SLOTS"]["SLOT_PRICE"])
        self.payout = 0
        self.jackpot = False
        self.is_vip = False
        self.reels = []
        self.currency_name = config["DEFAULT"]["CURRENCY_NAME"]

        self.do_work()

    def calculate_earnings(self):
        emotes = self.my_emotes.get_all_data()
        counts = Counter(self.reels)

        for i in counts:
            if counts[i] > 1:
                self.payout += int(emotes[i]) * int(counts[i])

        if self.jackpot:
            jackpot_mult = int(config["SLOTS"]["jackpot_multiplier"])
            self.payout *= jackpot_mult
        else:
            self.score_after -= self.slot_price

        multiplier = int(config["SLOTS"]["MULTIPLIER"])
        """If multiplier is 1 and user is VIP double their payout."""
        if multiplier == 1:
            self.is_vip = is_vip(self.channel[1:], self.user)
            if self.is_vip:
                self.payout *= (2 * multiplier)

        self.payout *= multiplier
        self.score_after += self.payout

    def do_message(self):
        reels = " ".join(self.reels)

        if self.jackpot:
            msg = f"JACKPOT! {self.user} got {reels}, {self.user} won " \
                  f"{str(self.payout)} {self.currency_name}!"
            logging.info(msg)
            self.send_message(msg)
            self.send_whisper(msg, self.user)
        else:
            msg = f"{reels} You won: {str(self.payout)}. You have: " \
                  f"{str(self.score_after)} {self.currency_name}!"
            logging.info(msg)
            self.send_whisper(msg, self.user)

    def do_work(self):
        self.spin_reels()
        self.is_jackpot()
        self.calculate_earnings()
        if self.score != self.score_after:
            self.my_users.set_value(self.user, self.score_after)
        self.do_message()

    def is_jackpot(self):
        self.jackpot = len(set(self.reels)) == 1

    def spin_reels(self) -> list:
        emotes = self.my_emotes.get_all_data()
        num_reels = int(config["SLOTS"]["NUM_REELS"])
        key_list = list(dict.keys(emotes))
        for i in range(num_reels):
            self.reels.append(choice(key_list))
