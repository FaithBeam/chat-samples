from requests import get


def get_channel_users(channel: str) -> list:
    """Returns a list of users in the channel."""
    url = f"https://tmi.twitch.tv/group/user/{channel}/chatters"

    users = get(url).json()
    try:
        mods = users["chatters"]["moderators"]
        viewers = users["chatters"]["viewers"]
        vips = users["chatters"]["vips"]
    except KeyError:
        return [""]

    return mods + viewers + vips


def get_user_group(channel: str, user: str) -> str:
    url = f"https://tmi.twitch.tv/group/user/{channel}/chatters"
    users = get(url).json()
    for group, user_list in users["chatters"].items():
        if user in user_list:
            return group
    return ""


def is_broadcasting(channel: str, client_id: str) -> bool:
    """Returns a bool if the channel is broadcasting.

    :param channel: Name of the channel.
    :param client_id: Your account's
    client-id. Look at "Getting a Client ID" here:
    https://dev.twitch.tv/docs/v5
    :return: A bool if the channel is
    broadcasting.
    """
    url = f"https://api.twitch.tv/helix/streams/?user_login={channel}"
    headers = {"Client-ID": client_id}

    result = (get(url, headers=headers).json()).get("data")
    if result:
        return True
    else:
        return False


def is_vip(channel: str, user: str) -> bool:
    group = get_user_group(channel, user)
    if group == "vips":
        return True
    else:
        return False
