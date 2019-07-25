import logging

from chatcommands.chatcommand import ChatCommand
from commands import Commands


class CustCommands(ChatCommand):
    """
    !commands
    Returns a list of all commands.
    """

    def __init__(self, whisper_cmds, public_cmds, privileged_cmds, c, channel):
        super().__init__(c, channel)
        self.whisper_cmds = whisper_cmds.copy()
        self.public_cmds = public_cmds.copy()
        self.privileged_cmds = privileged_cmds.copy()
        self.do_work()

    def do_work(self):
        my_custom_commands = Commands()
        whispers = self.do_thing(self.whisper_cmds)
        publics = self.do_thing(self.public_cmds)
        privs = self.do_thing(self.privileged_cmds)
        tmp = my_custom_commands.get_commands()

        msg = ", ".join([tmp, whispers, publics, privs])
        logging.info(msg)
        self.send_message(msg)

    @staticmethod
    def do_thing(my_list):
        for i in range(len(my_list)):
            my_list[i] = "!" + my_list[i]
        return ", ".join(my_list)
