from sqlalchemy import desc


class DatabaseConnection:
    def __init__(self, table_name, session):
        self.table_name = table_name
        self.session = session

    def bottom(
            self,
            column: str,
            limit=3
    ):
        return self.session.query(self.table_name) \
            .order_by(getattr(self.table_name, column))\
            .limit(limit)

    def count_records(self):
        return self.session.query(self.table_name).count()

    def delete_record(
            self,
            column: str,
            value
    ):
        self.session.delete(self.get_record(column, value))
        self.session.commit()

    def get_record(
            self,
            column: str,
            value
    ):
        return self.session.query(self.table_name)\
            .filter(getattr(self.table_name, column).like(value))\
            .first()

    def get_all_records(self):
        return self.session.query(self.table_name)

    def insert_record(self, data):
        self.session.add(data)
        self.session.commit()

    def top(
            self,
            column: str,
            limit=3
    ):
        return self.session.query(self.table_name)\
            .order_by(desc(getattr(self.table_name, column)))\
            .limit(limit)

    def update_record(
            self,
            column: str,
            value,
            set: dict
    ):
        self.session.query(self.table_name)\
            .filter(getattr(self.table_name, column) == value)\
            .update(set)
        self.session.commit()
