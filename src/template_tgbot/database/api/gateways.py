import typing
from sqlalchemy import select
from src.template_tgbot.database.models.account import User
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import suppress
from datetime import datetime
from typing import List, Dict
class BaseGateway:
    def __init__(self, session):
        self.session = session


class Gateway(BaseGateway):

    async def merge(self, model):
        async with self.session() as s:
            await s.merge(model)
            await s.commit()

    async def delete(self, model):
        async with self.session() as s:
            await s.delete(model)
            await s.commit()

    @property
    def user(self):
        return UserGateway(self.session)


class UserGateway(BaseGateway):
    async def get_by_chat_id(self, session: AsyncSession, chat_id: int) -> User:
        async with self.session as s:
            user = await s.get(User, chat_id)
            return user

    async def get_all(self) -> typing.Iterable[User]:
        async with self.session() as s:
            users = await s.execute(select(User))
        return users.scalars()

    async def create_new_user(self, chat_id: int, username: str) -> User:
        async with self.session() as s:
            user = await s.merge(User(id=chat_id, username=username))
            await s.commit()
        return user


async def get_games_by_id(session: AsyncSession, user_id: int) -> List[User]:
    game_data_request = await session.execute(
        select(User).where(User.id == user_id)
    )
    return game_data_request.scalars().all()

async def log_user(session: AsyncSession, chat_id: int, username: str):
    entry = User
    entry.username = username
    entry.id = chat_id
    with suppress(IntegrityError):
        await session.commit()