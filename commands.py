from template import Template
import models.models


class Commands(Template):
    def __init__(self, col_names=('Command Name', 'Message')):
        super().__init__(models.models.Commands, models.models.CommandsSchema, col_names)

    def get_commands(self) -> str:
        """Returns a list of all command names separated by commas,
        and prepended with exclamation marks."""
        result = list(self.get_all_data())
        result = " ".join(list(map("!{0},".format, result)))
        return result[:-1]
