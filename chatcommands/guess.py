import logging
import random

from chatcommands.chatcommand import ChatCommand
from config import config
from db_connection_utilities import DbConnectionUtilities
from models.models import Score, ScoreSchema


logging.getLogger(__name__)


class Guess(ChatCommand):
    """
    !guess <1-100>

    Play the guessing game. The guessing game is free to play.
    The default is to allow 1-100 but the max guess can be changed in
    config/config.ini.
    """

    def __init__(self, user: str, guess: str, auth_user, c, channel: str):
        super().__init__(c, channel)
        self.user = user
        self.guess = guess
        self.auth_user = auth_user
        self.c = c
        self.channel = channel
        self.do_work()

    def do_work(self):
        currency_name = config["DEFAULT"]["CURRENCY_NAME"]
        bot_win_cooldown = int(config["GUESS"]["bot_win_cooldown"])
        user_guess_cooldown = int(config["GUESS"]["user_guess_cooldown"])

        if not self.auth_user.user_can_message("bot_guess", bot_win_cooldown, False):
            return
        if not self.auth_user.user_can_message(
            self.user + "_guess", user_guess_cooldown
        ):
            return

        my_users = DbConnectionUtilities(Score, ScoreSchema, ("username", "score"))
        payout = config["GUESS"]["PAYOUT"]
        max_guess = int(config["GUESS"]["MAX_GUESS"])

        if not self.guess.isdigit():
            msg = f"{self.guess} not valid."
            logging.info(msg)
            self.send_whisper(msg, self.user)
            return
        if not 1 <= int(self.guess) <= max_guess:
            msg = f"Number must be between 1-{max_guess}."
            logging.info(msg)
            self.send_whisper(msg, self.user)
            return

        rand_num = choose_num(max_guess)
        if int(self.guess) == rand_num:
            my_users.add_to_value(self.user, payout)
            msg = (
                f"WINNER! {self.user} guessed the number {rand_num}! Added "
                f"{payout} {currency_name}. {self.user} has "
                f"{str(my_users.get_value(self.user))}."
            )
            logging.info(msg)
            self.send_whisper(msg, self.user)
            self.send_message(msg)
        elif (rand_num - 2) <= int(self.guess) <= (rand_num + 2):
            consolation_prize = config["GUESS"]["CONSOLATION_PRIZE"]
            my_users.add_to_value(self.user, consolation_prize)
            msg = (
                f"Consolation prize! You chose {self.guess}, number was "
                f"{rand_num}. Added {consolation_prize} {currency_name}."
            )
            logging.info(msg)
            self.send_whisper(msg, self.user)
        elif (rand_num - 5) <= int(self.guess) <= (rand_num + 5):
            consolation_prize = "1"
            my_users.add_to_value(self.user, consolation_prize)
            msg = (
                f"Consolation prize! You chose {self.guess}, number was "
                f"{rand_num}. Added {consolation_prize} {currency_name}."
            )
            logging.info(msg)
            self.send_whisper(msg, self.user)
        else:
            msg = f"Number was {rand_num}, you chose {self.guess}."
            logging.info(msg)
            self.send_whisper(msg, self.user)


def choose_num(max_num: int) -> int:
    return random.randint(1, max_num)
