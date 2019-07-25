Readme
======

`Docs <https://chat-samples.readthedocs.io/en/master/index.html>`_

A `Twitch.tv <www.twitch.tv>`_ chat bot written in Python3 that uses
SQLite3 to store data.

Requirements
============

* `Python <https://www.python.org/downloads/>`_ >= 3.6
* `Requests <https://pypi.org/project/requests/>`_
* `IRC <https://pypi.org/project/irc/>`_

Installation
============

1. git clone https://github.com/FaithBeam/chat-samples.git
2. cd chat-samples
3. virtualenv venv
4. source venv/bin/activate
5. pip install irc requests marshmallow-sqlalchemy

Configuring
===========

Refer to `config/readme.md` for configuration. Credentials.ini is the only 
necessary edits.

Running
=======

::

    python twitchbot.py
