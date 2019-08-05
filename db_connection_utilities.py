from database_connection import DatabaseConnection
from config import session


class DbConnectionUtilities(DatabaseConnection):
    def __init__(self, table_name, schema, column_names: tuple, session=session):
        super().__init__(table_name, session)
        self.table_schema = schema()
        self.table_name = table_name
        self.fieldnames = column_names
        self.session = session

    def add_item(self, key: str, val):
        if self.item_exists(key):
            return f"{key} already exists."
        insert = self.table_schema.load(
            {self.fieldnames[0]: key, self.fieldnames[1]: val}
        ).data
        self.insert_record(insert)
        return f"Added {key}: {val}."

    def add_to_value(self, key: str, val: str):
        if not self.item_exists(key):
            return f"{key} doesn't exist."
        pre_val = self.get_value(key)
        set = {self.fieldnames[1]: int(pre_val) + int(val)}
        self.update_record(self.fieldnames[0], key, set)
        return (
            f"Added {val} to {key}. {key} now has " f"{str(int(pre_val) + int(val))}."
        )

    def delete_item(self, item_name: str) -> str:
        self.delete_record(self.fieldnames[0], item_name)
        return f"Deleted {item_name}."

    def get_all_data(self):
        data = self.get_all_records()
        if len(self.fieldnames) == 2:
            data_list = {}
            if data is None:
                return {}
            for row in data:
                data_list[getattr(row, self.fieldnames[0])] = getattr(
                    row, self.fieldnames[1]
                )
            return data_list
        elif len(self.fieldnames) == 1:
            if data is None:
                return []
            my_list = []
            for row in data:
                my_list.append(getattr(row, self.fieldnames[0]))
            return my_list

    def get_bottom(self, column: str) -> str:
        rows = self.bottom(column)
        result = ""
        for row in rows:
            result = "".join(
                [
                    result,
                    ", ",
                    getattr(row, self.fieldnames[0]),
                    ": ",
                    str(getattr(row, self.fieldnames[1])),
                ]
            )
        return result[2:]

    def get_items(self) -> str:
        """Returns self.data as a string for human consumption."""
        tmp = self.get_all_data()
        return ", ".join("{!s}: {!s}".format(k, v) for (k, v) in tmp.items())

    def get_items_descending(self, column: str, limit=3) -> str:
        """The same as get_top. CLean this up."""
        rows = self.top(column, limit)
        result = ""
        for row in rows:
            result = "".join(
                [
                    result,
                    ", ",
                    getattr(row, self.fieldnames[0]),
                    ": ",
                    str(getattr(row, self.fieldnames[1])),
                ]
            )
        return result[2:]

    def get_top(self, column: str, limit=3) -> str:
        """The same as get_items_descending. Clean this up."""
        rows = self.top(column, limit)
        result = ""
        for row in rows:
            result = "".join(
                [
                    result,
                    ", ",
                    getattr(row, self.fieldnames[0]),
                    ": ",
                    str(getattr(row, self.fieldnames[1])),
                ]
            )
        return result[2:]

    def get_value(self, key: str) -> str:
        if not self.item_exists(key):
            return f"{key} doesn't exist."
        result = self.get_record(self.fieldnames[0], key)
        return getattr(result, self.fieldnames[1])

    def item_exists(self, key: str):
        result = self.get_record(self.fieldnames[0], key)
        if result is not None:
            return True
        return False

    def set_value(self, key: str, val):
        if not self.item_exists(key):
            return f"{key} doesn't exist."
        self.update_record(self.fieldnames[0], key, {self.fieldnames[1]: val})
        return f"Set {key} to {val}."
