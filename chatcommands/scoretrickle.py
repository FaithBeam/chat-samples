import logging

from sqlalchemy.orm import scoped_session, sessionmaker

from config import config, engine
from models.models import Score, ScoreSchema
from template import Template
from twitchapi import get_channel_users, is_broadcasting


class ScoreTrickle:
    """
    Currency trickle. Everyone in chat with an account in the scores db gets
    1 currency every 600 seconds.
    """
    def __init__(self, channel: str, client_id: str):
        self.channel = channel
        self.client_id = client_id
        self.do_work()

    def do_work(self):
        # Create session because if we don't we get a
        # "sqlite3.ProgrammingError: SQLite objects created in a thread can
        # only be used in that same thread." Therefore, we must create our
        # own session for the score trickle.
        session = scoped_session(sessionmaker(bind=engine))
        my_users = Template(Score, ScoreSchema, ("username", "score"), session)
        trickle = config["TRICKLE"]["TRICKLE"]

        if is_broadcasting(self.channel, self.client_id):
            users = get_channel_users(self.channel)
            msg = "Trickling:"

            for user in users:
                if my_users.item_exists(user):
                    msg = " ".join([msg, user])
                    my_users.add_to_value(user, trickle)
            logging.info(msg)
