from sqlalchemy import Column, BigInteger, String
from src.template_tgbot.database.base import Base


class User(Base):
    __tablename__ = "users"
    id = Column(BigInteger, primary_key=True, unique=True)
    username = Column(String(32))
    