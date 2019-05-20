from yamlhandler import YamlHandler


class Template(YamlHandler):
    def __init__(
            self,
            file: str
    ):
        super().__init__(file)

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
        post_val = pre_val + int(val)
        self.insert_document(key, post_val)
        return f"Added {val} to {key}. {key} now has {str(post_val)}."

    def delete_item(self, item_name: str) -> str:
        if self.item_exists(item_name):
            self.delete_document(item_name)
            return f"Deleted {item_name}."
        else:
            return f"{item_name} doesn't exist."

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

    def get_bottom(self) -> str:
        return ", ".join(self.bottom())

    def get_items(self) -> str:
        """Returns self.data as a string for human consumption."""
        tmp = self.get_all_data()
        return ', '.join("{!s}: {!s}".format(k, v) for (k, v) in tmp.items())


    def get_top(
            self,
            limit=3
    ) -> str:
        tmp = self.top(limit)
        result = ""
        for row in tmp:
            key = next(iter(row.keys()))
            val = str(row[key])
            result = "".join([result, key, ": ", val, ", "])
        return result[0:-2]

    def get_value(
            self,
            key: str
    ) -> str:
        if self.item_exists(key):
            return self.get_document(key)
        else:
            return f"{key} doesn't exist."

    def item_exists(
            self,
            key: str
    ):
        try:
            self.get_document(key)
            return True
        except KeyError:
            return False

    def set_value(
            self,
            key: str,
            val
    ):
        if not self.item_exists(key):
            return f"{key} doesn't exist."
        self.insert_document(key, val)
        return f"Set {key} to {val}."
