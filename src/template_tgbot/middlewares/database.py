
from typing import Callable, Awaitable, Dict, Any

from aiogram.types import Message
from aiogram import BaseMiddleware


class DatabaseMiddleware(BaseMiddleware):
    skip_patterns = ['error', 'update']

    def __init__(self, session):
        super().__init__()
        self.session = session

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        async with self.session() as session:
            data["session"] = session
        return await handler(event, data)
