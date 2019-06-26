from config import session, engine
from database_connection import DatabaseConnection
from models import Score, ScoreSchema


def main():
    db_con = DatabaseConnection(Score)
    tmp = db_con.get_row("username", "test")
    print(tmp.username)


    # score = Score(username="test", score=500)
    # score_schema = ScoreSchema()
    # column = "username"
    # value = "test"
    # query = "select * from scores where username=:username"
    # db_name = Score
    # print()

    # with engine.connect() as connection:
    #     rows = connection.execute(query, username=value)
    #     for row in rows:
    #         result_row = {}
    #         for col in row.keys():
    #             result_row[str(col)] = str(row[col])
    #     print(result_row)
    # if not result:
    #     session.add(score)
    #     session.commit()
    # dump_data = score_schema.dump(score).data
    # print(dump_data)
    # print(score_schema.load(dump_data, session=session).data)


if __name__ == '__main__':
    main()