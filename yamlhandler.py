from typing import List

import yaml


class YamlHandler:
    def __init__(
            self,
            file: str
    ):
        self.file = file
        with open(file, 'r') as f:
            yaml_file = yaml.safe_load(f)
        self.yaml_file = yaml_file

    def bottom(
            self,
            limit=3
    ) -> List[str]:
        current = self.yaml_file.copy()
        my_list = []
        for i in range(limit):
            min_key, min_val = min(current.items(), key=lambda x:x[1])
            current.pop(min_key)
            my_list.append(f"{min_key}: {min_val}")
        return my_list

    def count_documents(self) -> int:
        return len(self.yaml_file)

    def delete_document(
            self,
            key: str
    ):
        self.yaml_file.pop(key, None)
        self._write_yaml()

    def get_document(
            self,
            key: str
    ):
        return self.yaml_file[key]

    def get_all_documents(self) -> list:
        tmp_list = []
        tmp = self.db[self.collection_name].find()
        for row in tmp:
            tmp_list.append(row)
        return tmp_list

    def insert_document(
            self,
            key: str,
            val
    ):
        self.yaml_file[key] = val
        self._write_yaml()

    def top(
            self,
            limit=3
    ):
        current = self.yaml_file.copy()
        my_list = []
        for i in range(limit):
            max_key, max_val = max(current.items(), key=lambda x:x[1])
            current.pop(max_key)
            my_list += [max_key, max_val]
        return my_list

    def _write_yaml(self):
        with open(self.file, 'w') as f:
            yaml.safe_dump(self.yaml_file, f, default_flow_style=False)


if __name__ == "__main__":
    my_yaml = YamlHandler("test.yaml")
    print(my_yaml.bottom())
