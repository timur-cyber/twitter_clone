import datetime
import os

from sqlalchemy import (
    ARRAY,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    create_engine,
)
from sqlalchemy.orm import Session, declarative_base, sessionmaker
from sqlalchemy.sql import exists

if os.environ.get("DATABASE_URL"):
    DATABASE_URL = os.environ.get("DATABASE_URL")
else:
    DATABASE_URL = "postgresql+psycopg2://admin:admin@localhost/twitter"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
session: Session = SessionLocal()

Base = declarative_base(bind=engine)


class User(Base):
    """
    Таблица пользователей
    """

    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    api_key = Column(String, nullable=False, unique=True)


class Tweet(Base):
    """
    Таблица твитов
    """

    __tablename__ = "tweet"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(ForeignKey("user.id"), index=True)
    text = Column(String, index=True)
    media = Column("data", ARRAY(Integer), nullable=True)
    datetime = Column(DateTime(timezone=True), default=datetime.datetime.utcnow)


class Media(Base):
    """
    Таблица медиа файлов
    """

    __tablename__ = "media"
    id = Column(Integer, primary_key=True, index=True)
    link = Column(String, index=True)


class Like(Base):
    """
    Таблица лайков
    """

    __tablename__ = "like"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(ForeignKey("user.id"), index=True)
    tweet_id = Column(Integer, ForeignKey("tweet.id", ondelete="CASCADE"))


class Follow(Base):
    """
    Таблица подписок
    """

    __tablename__ = "follow"
    id = Column(Integer, primary_key=True, index=True)
    following_user_id = Column(ForeignKey("user.id"), index=True)
    followed_user_id = Column(ForeignKey("user.id"), index=True)


if __name__ == "__main__":
    # Создание тестовых данных
    if not session.query(exists().where(User.api_key == "test")).scalar():
        new_user = User(name="hello", api_key="test")
        session.add(new_user)
        session.commit()
    if not session.query(exists().where(User.api_key == "test2")).scalar():
        new_user_2 = User(name="world", api_key="test2")
        session.add(new_user_2)
        session.commit()
