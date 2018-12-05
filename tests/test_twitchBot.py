from unittest import TestCase
from unittest.mock import patch

from irc.client import Event


with patch('logging.basicConfig') as mocked_bc:
    with patch('configparser.ConfigParser') as mocked_cp:
        with patch('irc.bot.SingleServerIRCBot.__init__') as mocked_bot:
            with patch('repeatedtimer.RepeatedTimer') as rt:
                from twitchbot import TwitchBot


class TestTwitchBot(TestCase):
    def test_on_pubmsg(self):
        self.fail()

    def test_on_welcome(self):
        self.fail()

    def test__do_privileged_cmd(self):
        self.fail()

    def test__do_public_cmd(self):
        self.fail()

    def test__do_whisper_cmd(self):
        self.fail()

    def test__get_quote_number(self):
        num = "2"
        my_event = Event(arguments=[f"!quote {num}"], type="", source="",
                         target="")
        assert self.my_twitchbot._get_quote_number(my_event) == int(num) - 1

        num = "-1"
        my_event = Event(arguments=[f"!quote {num}"], type="", source="",
                         target="")
        assert self.my_twitchbot._get_quote_number(my_event) == -1

    def test__get_rank(self):
        my_event = Event(tags=[{'value': 'moderator/1'}], type="",
                         source="", target="")
        assert self.my_twitchbot._get_rank(my_event, "") == 2

        my_event = Event(tags=[{'value': 'broadcaster/1'}], type="",
                         source="", target="")
        assert self.my_twitchbot._get_rank(my_event, "") == 1

    def test__get_command(self):
        cmd = "mycmd"
        my_event = Event(arguments=[f"!{cmd}"], type="", source="",
                         target="")
        assert self.my_twitchbot._get_command(my_event) == cmd

    def test__get_quote(self):
        quote = "test quote"
        my_event = Event(arguments=[f"!addquote {quote}"], type="", source="",
                         target="")
        assert self.my_twitchbot.get_quote(my_event) == quote

        my_event = Event(arguments=[f"!addquote"], type="", source="",
                         target="")
        assert self.my_twitchbot.get_quote(my_event) is False

    def test__get_second_word(self):
        scd_wrd = "second"
        my_event = Event(arguments=[f"!cmd {scd_wrd}"], type="", source="",
                         target="")
        assert self.my_twitchbot._get_second_word(my_event) == scd_wrd

        scd_wrd = "second"
        my_event = Event(arguments=[f"!cmd {scd_wrd} third"], type="",
                         source="",
                         target="")
        assert self.my_twitchbot._get_second_word(my_event) == scd_wrd

        my_event = Event(arguments=[f"!cmd"], type="", source="", target="")
        assert self.my_twitchbot._get_second_word(my_event) == -1

    def test__get_username(self):
        usern = "test"
        my_event = Event(source=f"{usern}!after", type="", target="")
        assert self.my_twitchbot._get_username(my_event) == usern

    def test__is_broadcaster(self):
        my_event = Event(tags=[{'value': 'broadcaster/1'}], type="",
                         source="", target="")
        assert self.my_twitchbot._is_broadcaster(my_event) is True

        my_event = Event(tags=[{'value': 'other/1'}], type="",
                         source="", target="")
        assert self.my_twitchbot._is_broadcaster(my_event) is False

    def test__is_command(self):
        my_event = Event(arguments=["!cmd"], type="", source="", target="")
        assert self.my_twitchbot._is_command(my_event) is True

        my_event = Event(arguments=["cmd"], type="", source="", target="")
        assert self.my_twitchbot._is_command(my_event) is False

        my_event = Event(arguments=["cmd !cmd"], type="", source="", target="")
        assert self.my_twitchbot._is_command(my_event) is False

    def test__is_moderator(self):
        my_event = Event(tags=[{'value': 'moderator/1'}], type="",
                         source="", target="")
        assert self.my_twitchbot._is_moderator(my_event) is True

        my_event = Event(tags=[{'value': 'other/1'}], type="",
                         source="", target="")
        assert self.my_twitchbot._is_moderator(my_event) is False

    def test__is_whisper(self):
        target = "user"
        assert self.my_twitchbot._is_whisper(target) is True

        target = "#channel"
        assert self.my_twitchbot._is_whisper(target) is False

    def test__message_word_count(self):
        assert self.my_twitchbot._message_word_count("one two three") == 3
        assert self.my_twitchbot._message_word_count("one two") == 2

    def test__parse_custom_cmd(self):
        cmd = "testcom"
        text = "is a new command!"
        my_event = Event(arguments=[f"addcom {cmd} {text}"], source="", target="",
                         type="")
        assert self.my_twitchbot._parse_custom_cmd(my_event) == [cmd, text]

        cmd = "test-com"
        text = "is a new command!"
        my_event = Event(arguments=[f"addcom {cmd} {text}"], source="",
                         target="",
                         type="")
        assert self.my_twitchbot._parse_custom_cmd(my_event) is False

    def setUp(self):
        self.username = "test-usrn"
        self.client_id = "test-client-id"
        self.oauth = "test-oauth"
        self.channel = "test-channel"
        self.my_twitchbot = TwitchBot(self.username, self.client_id, self.oauth,
                             self.channel)

    def tearDown(self):
        del self.username
        del self.client_id
        del self.oauth
        del self.channel
        del self.my_twitchbot
