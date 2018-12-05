from unittest import TestCase

import httpretty

import twitchapi


def pretty_get(url, body):
    httpretty.register_uri(
        httpretty.GET,
        url,
        body=body
    )


class TestTwitchApi(TestCase):
    @httpretty.activate
    def test_get_channel_users(self):
        channel = "jhbddfg"
        url = f"https://tmi.twitch.tv/group/user/{channel}/chatters"

        body = '{"chatters": {"moderators": ["test-mod"], "viewers": ' \
               '["test-viewer"], "vips": ["test-vip"]}}'
        pretty_get(url, body)
        assert twitchapi.get_channel_users(channel) == [
            "test-mod", "test-viewer", "test-vip"
        ]

        body = '{"chatters": {"moderators": [], "viewers": [], "vips": []}}'
        pretty_get(url, body)
        assert twitchapi.get_channel_users(channel) == []

    @httpretty.activate
    def test_is_broadcasting(self):
        client_id = "bwgsy294cvd93af284g9vuilezgijy"
        channel = "shdbgsh"
        url = f"https://api.twitch.tv/helix/streams/?user_login={channel}"

        body = '{"data": [], "pagination": []}'
        pretty_get(url, body)
        assert twitchapi.is_broadcasting(channel, client_id) is False

        body = '{"data": ["test"], "pagination": []}'
        pretty_get(url, body)
        assert twitchapi.is_broadcasting(channel, client_id) is True
