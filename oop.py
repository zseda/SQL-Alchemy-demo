"""
credits from: https://github.com/ArjanCodes/

"""

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, sessionmaker, declarative_base
from loguru import logger

# create db engine
db = sa.create_engine("sqlite:///:memory:")

# bind db to a session
Session = sessionmaker(bind=db)

# Base class to use for actual tables
Base = declarative_base()


# Classes that inherit from Base will be mapped to tables
class User(Base):
    __tablename__ = "users"
    # Mapped is a type hint for the column
    id: Mapped[int] = mapped_column(primary_key=True, index=True, unique=True)
    username: Mapped[str]
    email: Mapped[str]

    # wrapper method developer friendly representation of the object
    def __repr__(self) -> str:
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"


def main() -> None:
    # create all with base class and metadata schematic
    Base.metadata.create_all(db)
    # create instance of the user class
    user = User(username="zeynep", email="zeynep.birinci@hitec-hamburg.de")
    second_user = User(username="hitec-user", email="hitec-user@hitec-hamburg.de")
    # session to interact with the db
    with Session() as session:
        session.add(user)
        session.add(second_user)
        session.commit()
        logger.info((session.query(User).all()))


if __name__ == "__main__":
    main()
