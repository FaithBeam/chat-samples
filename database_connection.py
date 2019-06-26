from config import session


class DatabaseConnection:
    def __init__(self, table_name):
        self.table_name = table_name

    def bottom(
            self,
            field: str
    ):
        return self.db[self.table_name]\
            .find()\
            .sort(field, ASCENDING)\
            .limit(3)

    def count_documents(self):
        return self.db[self.table_name].count()

    def delete_document(
            self,
            data: dict
    ):
        return self.db[self.table_name].delete_one(data).deleted_count

    def get_row(
            self,
            column: str,
            value
    ):
        return session.query(self.table_name).filter(getattr(self.table_name, column).like(value)).first()

    def get_all_documents(self) -> list:
        tmp_list = []
        tmp = self.db[self.table_name].find()
        for row in tmp:
            tmp_list.append(row)
        return tmp_list

    def insert_document(
            self,
            data: dict
    ):
        return self.db[self.table_name].insert_one(data).inserted_id

    def top(
            self,
            field: str,
            limit=3
    ):
        return self.db[self.table_name]\
            .find()\
            .sort(field, DESCENDING)\
            .limit(limit)

    def update_document(
            self,
            search: dict,
            set_data: dict
    ):
        return self.db[self.table_name]\
            .replace_one(search, set_data)\
            .modified_count
