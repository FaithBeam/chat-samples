Readme
======

A `Twitch.tv <www.twitch.tv>`_ chat bot written in Python3 that uses
`MongoDB <https://www.mongodb.com/>`_ to store data.

Requirements
============

* `Python <https://www.python.org/downloads/>`_ >= 3.6
* A `MongoDB <https://www.mongodb.com/>`_ instance
* `Requests <https://pypi.org/project/requests/>`_
* `IRC <https://pypi.org/project/irc/>`_
* `PyMongo <https://pypi.org/project/pymongo/>`_

Installation
============

**Installing MongoDB**

`Installation <https://docs.mongodb.com/manual/installation/>`_

**Installing the bot**
::

    git clone https://github.com/FaithBeam/chat-samples.git
    cd chat-samples
    virtualenv venv
    source venv/bin/activate
    pip install irc requests pymongo

Configuring
===========

Refer to `config/readme.md` for configuration. Credentials.ini is the only 
necessary edits unless you installed your mongodb instance on another machine.

Running
=======

::

    python twitchbot.py