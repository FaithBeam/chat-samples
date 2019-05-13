import yaml
from collections import Counter


class YamlHandler:
    def __init__(
        self,
        file: str
    ):
        self.file = file
        with open(file, 'a+') as f:
            data = f.read
        self.yaml_file = yaml.load(data)

    def bottom(
            self,
            field: str
    ):
        return self.db[self.collection_name]\
            .find()\
            .sort(field, ASCENDING)\
            .limit(3)

    def count_documents(self) -> int:
        return len(self.yaml_file)

    def delete_document(
            self,
            key: str
    ):
        self.yaml_file.pop(key, None)
        yaml.dump(self.yaml_file, self.file)

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
        yaml.dump(self.yaml_file, self.file)

    def top(
            self,
            field: str,
            limit=3
    ):
        return Counter(self.yaml_file).most_common(3)
