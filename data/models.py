from sqlalchemy import (BigInteger, String, DateTime, func, Integer,
                        MetaData)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

metadata = MetaData()


class BaseModelBot(DeclarativeBase):
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())


class Room(BaseModelBot):
    __tablename__ = "Rooms"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str] = mapped_column(String(250), nullable=False)
    photo: Mapped[str] = mapped_column(String(250), nullable=False)


class User(BaseModelBot):
    __tablename__ = 'Users'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_first_name: Mapped[str] = mapped_column(String(150), nullable=False)
    user_id: Mapped[BigInteger] = mapped_column(BigInteger, nullable=False, unique=True)
    user_url: Mapped[str] = mapped_column(String(150))
