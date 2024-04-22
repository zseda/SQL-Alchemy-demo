"""
credits from: https://github.com/ArjanCodes/

"""

import hashlib
import typing
import sqlalchemy as sa
from sqlalchemy.orm import (
    declarative_base,
    mapped_column,
    relationship,
    sessionmaker,
    Mapped,
)
from loguru import logger

db = sa.create_engine("sqlite:///:memory:")
Session = sessionmaker(bind=db)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    # one to one relationship with UserAuth
    # back_populates is both sided relationship
    # uselist=False means one to one relationship
    auth: Mapped["UserAuth"] = relationship(
        "UserAuth", uselist=False, back_populates="user"
    )
    # one to many relationship with UserPost
    posts: Mapped[typing.List["UserPost"]] = relationship(
        "UserPost", back_populates="user"
    )

    def __init__(self, username: str, email: str, password: str):
        super().__init__()
        self.auth = UserAuth(username=username, email=email)
        self.auth.set_password(password)

    def __repr__(self) -> str:
        return f"<User(username={self.auth.username}, email={self.auth.email})>"


class UserAuth(Base):
    __tablename__ = "user_auth"
    # Mapped is a type hint for the column sa.Integer is the type of the column in db
    id: Mapped[int] = mapped_column(
        sa.Integer, sa.ForeignKey("users.id"), primary_key=True, index=True, unique=True
    )
    username: Mapped[str]
    email: Mapped[str] = mapped_column(index=True, unique=True)
    password_hash: Mapped[str]
    user: Mapped["User"] = relationship("User", back_populates="auth")

    def __init__(self, username: str, email: str):
        self.username = username
        self.email = email

    # add behaviour to the table
    def set_password(self, password: str) -> None:
        self.password_hash = hashlib.sha256(password.encode()).hexdigest()

    def check_password(self, password: str) -> bool:
        return self.password_hash == hashlib.sha256(password.encode()).hexdigest()

    def __repr__(self) -> str:
        return f"<UserAuth(username={self.username}, email={self.email})>"


class UserPost(Base):
    __tablename__ = "user_posts"
    id: Mapped[int] = mapped_column(primary_key=True)
    # want to make sure that user_id is not null
    # index to find the user post faster
    user_id: Mapped[int] = mapped_column(
        sa.Integer, sa.ForeignKey("users.id"), nullable=False, index=True
    )
    content: Mapped[str]
    user: Mapped["User"] = relationship("User", back_populates="posts")

    def __repr__(self) -> str:
        return f"<UserPost(user={self.user}, content={self.content})>"


def main() -> None:
    Base.metadata.create_all(db)

    with Session.begin() as session:
        user = User(
            username="zeynep",
            email="zeynep.birinci@hitec-hamburg.de",
            password="password",
        )
        post = UserPost(content="Hello World!", user=user)
        session.add(user)
        session.add(post)

    with Session.begin() as session:
        user = session.query(User).first()
        logger.info(user)
        logger.info(user.auth)
        logger.info(user.posts)

        logger.info(f"Password check: {user.auth.check_password('password')}")
        logger.info(f"Password check: {user.auth.check_password('wrongpassword')}")
        # filter posts by user
        posts = session.query(UserPost).filter(UserPost.user == user).all()
        logger.info(posts)


if __name__ == "__main__":
    main()
