from template import Template


class Commands(Template):
    def __init__(
            self,
            table_name="commands",
            col_names=('Command Name', 'Message')
    ):
        super().__init__(table_name, col_names)

    def get_commands(self) -> str:
        """Returns a list of all command names separated by commas,
        and prepended with exclamation marks."""
        result = list(self.get_all_data())
        result = " ".join(list(map("!{0},".format, result)))
        return result[:-1]
