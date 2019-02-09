from pymongo import ASCENDING, DESCENDING, MongoClient

from config import config


class MongoCon:
    def __init__(
            self,
            collection_name,
    ):
        self.collection_name = collection_name
        self.address = config["MONGODB"]["IP"]
        self.port = config["MONGODB"]["PORT"]
        self.client = MongoClient(f'{self.address}:{self.port}')
        self.db = self.client.TwitchBot

    def bottom(
            self,
            field: str
    ):
        return self.db[self.collection_name].find().sort(
            field, ASCENDING
        ).limit(3)

    def count_documents(self):
        return self.db[self.collection_name].count()

    def delete_document(
            self,
            data: dict
    ):
        return self.db[self.collection_name].delete_one(data).deleted_count

    def get_document(
            self,
            search: dict
    ):
        return self.db[self.collection_name].find_one(search)

    def get_all_documents(self) -> list:
        tmp_list = []
        tmp = self.db[self.collection_name].find()
        for row in tmp:
            tmp_list.append(row)
        return tmp_list

    def insert_document(
            self,
            data: dict
    ):
        return self.db[self.collection_name].insert_one(data).inserted_id

    def top(
            self,
            field: str,
            limit=3
    ):
        return self.db[self.collection_name].find().sort(
            field, DESCENDING
        ).limit(limit)

    def update_document(
            self,
            search: dict,
            set_data: dict
    ):
        return self.db[self.collection_name]\
            .replace_one(search, set_data)\
            .modified_count
