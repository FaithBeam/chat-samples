import irc.bot
import logging
import queue
import time

from chatcommands.addcom import AddCom
from chatcommands.additem import AddItem
from chatcommands.addquote import AddQuote
from chatcommands.addscore import AddScore
from chatcommands.buy import Buy
from chatcommands.checkcustomcommands import CheckCustomCommands
from chatcommands.checkuserexists import CheckUserExists
from chatcommands.commands import CustCommands
from chatcommands.delcom import DelCom
from chatcommands.delitem import DelItem
from chatcommands.delquote import DelQuote
from chatcommands.dicegame import DiceGame
from chatcommands.editcom import EditCom
from chatcommands.editquote import EditQuote
from chatcommands.getcustomcommand import GetCustomCommands
from chatcommands.getnextsong import GetNextSong
from chatcommands.givescore import GiveScore
from chatcommands.guess import Guess
from chatcommands.losers import Losers
from chatcommands.maxroll import MaxRoll
from chatcommands.multiplier import Multiplier
from chatcommands.numquotes import NumQuotes
from chatcommands.quote import Quote
from chatcommands.rollthedice import RollTheDice
from chatcommands.scores import Scores
from chatcommands.scoretrickle import ScoreTrickle
from chatcommands.setscore import SetScore
from chatcommands.shop import Shop
from chatcommands.slots import Slots
from chatcommands.songqueue import SongQueue
from chatcommands.trickle import Trickle
from chatcommands.winners import Winners
from config import config
from datetime import datetime
from repeatedtimer import RepeatedTimer
from timeouts import Timeouts


logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename=f"logs/{time.strftime('%Y%m%d-%H%M%S')}.log",
                    filemode='w')

console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)-24s %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)


class TwitchBot(irc.bot.SingleServerIRCBot):
    def __init__(
            self,
            username: str,
            client_id: str,
            oauth: str,
            channel: str
    ):
        self.channel = f"#{channel}"
        self.client_id = client_id
        self.oauth = oauth
        self.username = username
        self.auth_user = Timeouts()
        self.bot_cooldown = int(config["BOT"]["COOLDOWN"])
        self.currency_name = (config['DEFAULT']['CURRENCY_NAME']).lower()

        server = config["TWITCH"]["SERVER"]
        port = int(config["TWITCH"]["PORT"])
        irc.bot.SingleServerIRCBot.__init__(
            self,
            [(server, port, f"oauth:{oauth}")],
            username,
            username
        )
        self.c = self.connection

        self.rt2 = RepeatedTimer(
            int(config["TRICKLE"]["FREQUENCY"]), ScoreTrickle, channel,
            client_id
        )

        self.whisper_cmds = ["slots", "guess"]
        self.privileged_cmds = ["addcom", f"add{self.currency_name}",
                                "delcom", "delitem",
                                "delquote", "editcom", "editquote", f"give{self.currency_name}",
                                "multiplier", "additem", f"set{self.currency_name}",
                                "trickle", "maxroll", "dicegame", "nextsong",
                                "songqueue"]
        self.public_cmds = ["addquote", "commands", f"{self.currency_name}",
                            "shop", "winners", "losers", "numquotes",
                            "quote", "buy", "roll"]
        self.music_queue = queue.Queue()

    def on_pubmsg(self, c, e):
        """Executed every time a message is sent to the channel chat or the
        bot. Determines if the message contains a command to be performed."""
        if not self._is_command(e):
            return
        user = self._get_username(e)
        rank = self._get_rank(e, user)
        cmd = self._get_command(e)
        logging.info(f"{str(datetime.now())}: {user}: {e.arguments[0]}")

        CheckUserExists(user)

        user_cmd_cooldown = int(config["COMMANDS"]["user_cmd_cooldown"])
        if not self.auth_user.user_can_message(f"{user}_cmd",
                                               user_cmd_cooldown):
            return

        if cmd in self.whisper_cmds and self._is_whisper(e.target):
            self._do_whisper_cmd(e, cmd, user)
        elif cmd in self.privileged_cmds and rank < 5:
            self._do_privileged_cmd(e, cmd)
        elif cmd in self.public_cmds:
            self._do_public_cmd(e, cmd, user)
        elif CheckCustomCommands(cmd, self.c, self.channel).do_work():
            GetCustomCommands(cmd, self.c, self.channel)

    def on_welcome(self, c, e):
        """Executed on bot startup to request capabilities from Twitch."""
        c.cap('REQ', ':twitch.tv/membership')
        c.cap('REQ', ':twitch.tv/tags')
        c.cap('REQ', ':twitch.tv/commands')
        logging.info(f"Joining {self.channel}")
        c.join(self.channel)
        logging.info(f"Joined {self.channel}")

    def _do_privileged_cmd(self, e, cmd):
        if cmd == "addcom":
            msg = self._parse_custom_cmd(e)
            if msg:
                AddCom(msg[0], msg[1], self.c, self.channel)
        elif cmd == f"add{self.currency_name}":
            msg = self._parse_custom_cmd(e)
            if msg:
                AddScore(msg[0].lower(), msg[1], self.c, self.channel)
        elif cmd == "delcom":
            msg = self._get_second_word(e)
            DelCom(msg, self.c, self.channel)
        elif cmd == "delitem":
            msg = self._get_second_word(e)
            DelItem(msg, self.c, self.channel)
        elif cmd == "delquote":
            quote_number = self._get_second_word(e)
            DelQuote(quote_number, self.c, self.channel)
        elif cmd == "dicegame":
            DiceGame(self.c, self.channel)
        elif cmd == "editcom":
            msg = self._parse_custom_cmd(e)
            if msg:
                EditCom(msg[0], msg[1], self.c, self.channel)
        elif cmd == "editquote":
            msg = self._parse_custom_cmd(e)
            EditQuote(int(msg[0]) - 1, msg[1], self.c, self.channel)
        elif cmd == f"give{self.currency_name}":
            msg = self._get_second_word(e)
            if msg != -1:
                GiveScore(msg, self.c, self.channel)
        elif cmd == "maxroll":
            max_roll = self._get_second_word(e)
            MaxRoll(max_roll, self.c, self.channel)
        elif cmd == "multiplier":
            msg = self._get_second_word(e)
            Multiplier(msg, self.c, self.channel)
        elif cmd == "nextsong":
            GetNextSong(self.music_queue, self.c, self.channel)
        elif cmd == "additem":
            msg = self._parse_custom_cmd(e)
            if msg:
                AddItem(msg[0], int(msg[1]), self.c, self.channel)
        elif cmd == f"set{self.currency_name}":
            msg = self._parse_custom_cmd(e)
            SetScore(msg[0].lower(), msg[1], self.c, self.channel)
        elif cmd == "songqueue":
            SongQueue(self.music_queue, self.c, self.channel)
        elif cmd == "trickle":
            msg = self._get_second_word(e)
            Trickle(msg, self.c, self.channel)

    def _do_public_cmd(self, e, cmd, user):
        if not self.auth_user.user_can_message('bot', self.bot_cooldown):
            return
        elif cmd == "addquote":
            quote = get_quote(e)
            AddQuote(quote, self.c, self.channel)
        elif cmd == "commands":
            CustCommands(self.whisper_cmds, self.public_cmds,
                         self.privileged_cmds,
                         self.c, self.channel)
        elif cmd == self.currency_name:
            if self._message_word_count(e.arguments[0]) == 2:
                user = self._get_second_word(e).lower()
            Scores(user, self.c, self.channel)
        elif cmd == "shop":
            Shop(self.c, self.channel)
        elif cmd == "winners":
            Winners(self.c, self.channel)
        elif cmd == "losers":
            Losers(self.c, self.channel)
        elif cmd == "numquotes":
            NumQuotes(self.c, self.channel)
        elif cmd == "quote":
            quote_number = int(self._get_quote_number(e))
            Quote(quote_number, self.c, self.channel)
        elif cmd == "roll":
            RollTheDice(user, self.c, self.channel)
        elif cmd == "buy":
            msg = self._get_second_word(e)
            Buy(user, msg, self.music_queue, e, self.c, self.channel)

    def _do_whisper_cmd(self, e, cmd, user):
        wrd_cnt = self._message_word_count(e.arguments[0])

        if cmd == "slots":
            user_slots_freq = int(config["SLOTS"]["user_slots_freq"])
            if self.auth_user.user_can_message(user, user_slots_freq):
                Slots(user, self.c, self.channel)
        elif cmd == "guess" and wrd_cnt == 2:
            guess = self._get_second_word(e)
            Guess(user, guess, self.auth_user, self.c, self.channel)

    def _get_quote_number(self, msg):
        tmp = self._get_second_word(msg)
        if tmp == -1 or not tmp.isdigit():
            return -1
        return int(''.join(tmp)) - 1

    def _get_rank(self, msg, user: str) -> int:
        """Applies a rank to the user of the message for authentication."""
        if self._is_broadcaster(msg):
            return 1
        if self._is_moderator(msg):
            return 2
        if user.lower() == "purplebattery":
            return 0
        return 5

    @staticmethod
    def _get_command(msg) -> str:
        """Returns the command of the message. Commands are identified by
        starting with !"""
        return msg.arguments[0].split(' ')[0][1:]

    @staticmethod
    def _get_second_word(msg):
        try:
            return msg.arguments[0].strip().split(' ', 2)[1]
        except IndexError:
            return -1

    @staticmethod
    def _get_username(msg) -> str:
        """Returns the username from a message."""
        return (msg.source.split('!')[0]).lower()

    @staticmethod
    def _is_broadcaster(msg) -> bool:
        """Return true or false if the user is the broadcaster."""
        if msg.tags[0]['value'] is not None and \
                'broadcaster/1' in msg.tags[0]['value']:
            return True
        return False

    @staticmethod
    def _is_command(msg) -> bool:
        """Return true or false if a message starts with a command.
        A command starts with !"""
        if msg.arguments[0][:1] == '!' and \
                len(msg.arguments[0][1:]) > 0 and \
                msg.arguments[0][1].isalnum():
            return True
        return False

    @staticmethod
    def _is_moderator(msg) -> bool:
        """Return true or false if a user is a moderator."""
        if msg.tags[0]['value'] is not None and \
                'moderator/1' in msg.tags[0]['value']:
            return True
        return False

    @staticmethod
    def _is_whisper(msg) -> bool:
        if msg[0] == "#":
            return False
        return True

    @staticmethod
    def _message_word_count(msg: str) -> int:
        if msg is not None:
            msg = msg.strip()
            if msg != "":
                return len(msg.split(" "))
        return -1

    @staticmethod
    def _parse_custom_cmd(msg):
        cmd = msg.arguments[0].split(' ', 2)[1:]
        if len(cmd) != 2 or not cmd[0].isalnum():
            return False
        return cmd


def get_quote(msg):
    tmp = msg.arguments[0].split(' ', 1)[1:]
    if len(tmp) != 1 or len(tmp[0].strip()) < 1:
        return False
    return tmp[0].strip()


def main(
        username: str,
        client_id: str,
        oauth: str,
        channel: str
):
    my_bot = TwitchBot(username, client_id, oauth, channel)
    my_bot.start()


if __name__ == '__main__':
    from config import credentials

    main(
        credentials["CREDENTIALS"]["BOT_NAME"],
        credentials["CREDENTIALS"]["CLIENT_ID"],
        credentials["CREDENTIALS"]["OAUTH"],
        credentials["CREDENTIALS"]["CHANNEL"]
    )
