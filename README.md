# Python Twitchbot

A [Twitch.tv](www.twitch.tv) chat bot written in Python3 that uses
[MongoDB](https://www.mongodb.com/) to store data.

## Requirements

* [Python](https://www.python.org/downloads/) >= 3.6
* A [MongoDB](https://www.mongodb.com/) instance
* [Requests](https://pypi.org/project/requests/)
* [IRC](https://pypi.org/project/irc/)
* [PyMongo](https://pypi.org/project/pymongo/)

## Installation

**Installing MongoDB**

[Installation](https://docs.mongodb.com/manual/installation/)

**Installing the bot**

```
git clone https://github.com/FaithBeam/chat-samples.git
cd chat-samples
virtualenv venv
source venv/bin/activate
pip install irc requests pymongo
```

**Configuring the bot**

Refer to `config/readme.md` for configuration. Credentials.ini is the only 
necessary edits unless you installed your mongodb instance on another machine.