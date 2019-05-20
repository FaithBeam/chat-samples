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
        self.insert_document(key, val)
        return f"Added {key}: {val}."

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
        return self.get_all_documents()

    def get_bottom(self) -> str:
        return ", ".join(self.bottom())

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
