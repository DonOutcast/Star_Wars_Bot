import aiogram
from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.utils.markdown import hcode
from sqlalchemy.ext.asyncio import AsyncSession
from src.template_tgbot.database.api.gateways import get_games_by_id
echo_router = Router()

# @echo_router.message(aiogram.F)
# async def get_inf(message: types.Message):
#     await message.answer(text=message.json())

@echo_router.message(F.text)
async def bot_echo(message: types.Message, session: AsyncSession):
    text = [
        "Ехо без стану.",
        "Повідомлення:",
        message.text
    ]
    user = await get_games_by_id(session=session, user_id=message.chat.id)
    if user:
        await message.answer(f"Hi, {user}")
    await message.answer('\n'.join(text))


@echo_router.message(F.text)
async def bot_echo_all(message: types.Message, state: FSMContext):
    state_name = await state.get_state()
    text = [
        f'Ехо у стані {hcode(state_name)}',
        'Зміст повідомлення:',
        hcode(message.text)
    ]
    await message.answer('\n'.join(text))

