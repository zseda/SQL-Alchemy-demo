"""
credits from: https://github.com/ArjanCodes/

"""

import sqlalchemy as sa
from loguru import logger

# create db engine
engine = sa.create_engine("sqlite:///:memory:")
# logging detail for detail debugging
# engine.echo = True
# create db connection
connection = engine.connect()
# create meta data object
# allows us to define schema
metadata = sa.MetaData()

# create actual table
user_table = sa.Table(
    "user",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("username", sa.String),
    sa.Column("email", sa.String),
)


# insert user into table
def insert_user(username: str, email: str) -> None:
    query = user_table.insert().values(username=username, email=email)
    connection.execute(query)


def select_user(username: str) -> sa.engine.Result:
    query = user_table.select().where(user_table.c.username == username)
    result = connection.execute(query)
    return result.fetchone()


def main() -> None:
    # create all table
    metadata.create_all(engine)
    insert_user("zeynep", "zeynep.birinci@hitec-hamburg.de")
    logger.info((select_user("zeynep")))
    connection.close()


if __name__ == "__main__":
    main()
