from database_connection import DatabaseConnection


class Template(DatabaseConnection):
    def __init__(
            self,
            table_name: str,
            column_names: tuple
    ):
        super().__init__(table_name)
        self.fieldnames = column_names

    def add_item(
            self,
            key: str,
            val
    ):
        if self.item_exists(key):
            return f"{key} already exists."
        data = {self.fieldnames[0]: key, self.fieldnames[1]: val}
        result = self.insert_document(data)
        if result is not None:
            return f"Added {key}: {val}."
        return f"Couldn't add {key}."

    def add_to_value(
            self,
            key: str,
            val: str
    ):
        if not self.item_exists(key):
            return f"{key} doesn't exist."
        pre_val = self.get_value(key)
        search = {self.fieldnames[0]: key}
        data = {
            self.fieldnames[0]: key,
            self.fieldnames[1]: int(pre_val) + int(val)
        }
        if self.update_document(search, data) == 1:
            return (
                f"Added {val} to {key}. {key} now has "
                f"{str(int(pre_val) + int(val))}."
            )
        return f"Couldn't add {val} to {key}."

    def delete_item(self, item_name: str) -> str:
        result = self.delete_document({self.fieldnames[0]: item_name})
        if result == 1:
            return f"Deleted {item_name}."
        return f"Didn't delete {item_name}."

    def get_all_data(self):
        data = self.get_all_documents()
        if len(self.fieldnames) == 2:
            data_list = {}
            if data is None:
                return {}
            for row in data:
                data_list[row[self.fieldnames[0]]] = row[self.fieldnames[1]]
            return data_list
        elif len(self.fieldnames) == 1:
            if data is None:
                return []
            my_list = []
            for row in data:
                my_list.append(row[self.fieldnames[0]])
            return my_list

    def get_bottom(
            self,
            field: str
    ) -> str:
        tmp = self.bottom(field)
        result = ""
        for row in tmp:
            result = "".join(
                 [result, ", ", row["Username"], ": ", str(row["Score"])]
            )
        return result[2:]

    def get_items(self) -> str:
        """Returns self.data as a string for human consumption."""
        tmp = self.get_all_data()
        return ', '.join("{!s}: {!s}".format(k, v) for (k, v) in tmp.items())

    def get_items_descending(
            self,
            field: str,
            limit=3
    ) -> str:
        tmp = self.top(field, limit)
        result = ""
        for row in tmp:
            result = "".join(
                 [result, ", ", row[self.fieldnames[0]], ": ",
                  str(row[self.fieldnames[1]])]
            )
        return result[2:]

    def get_top(
            self,
            field: str,
            limit=3
    ) -> str:
        tmp = self.top(field, limit)
        result = ""
        for row in tmp:
            result = "".join(
                 [result, ", ", row["Username"], ": ", str(row["Score"])]
            )
        return result[2:]

    def get_value(
            self,
            key: str
    ) -> str:
        if not self.item_exists(key):
            return f"{key} doesn't exist."
        data = {self.fieldnames[0]: key}
        result = self.get_row(data)
        return result[self.fieldnames[1]]

    def item_exists(
            self,
            key: str
    ):
        data = {self.fieldnames[0]: key}
        result = self.get_row(data)
        if result is not None:
            return True
        return False

    def set_value(
            self,
            key: str,
            val
    ):
        if not self.item_exists(key):
            return f"{key} doesn't exist."
        data = {self.fieldnames[0]: key, self.fieldnames[1]: val}
        search = {self.fieldnames[0]: key}
        result = self.update_document(search, data)
        if result == 1:
            return f"Set {key} to {val}."
        return f"Couldn't set {key} to {val}."
