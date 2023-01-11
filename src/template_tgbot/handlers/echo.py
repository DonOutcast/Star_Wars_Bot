import aiogram
from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.utils.markdown import hcode

echo_router = Router()

# @echo_router.message(aiogram.F)
# async def get_inf(message: types.Message):
#     await message.answer(text=message.json())

@echo_router.message(F.text)
async def bot_echo(message: types.Message):
    text = [
        "Ехо без стану.",
        "Повідомлення:",
        message.text
    ]

    await message.answer('\n'.join(text))
    await message.answer_photo("AgACAgIAAxkBAAMMY76zCyLEDC6F2r2hUN1rYx3eUmcAAmbFMRuWmPlJBA5dZn-DNR8BAAMCAANzAAMtBA")
    print(message.from_user.id)


@echo_router.message(F.text)
async def bot_echo_all(message: types.Message, state: FSMContext):
    state_name = await state.get_state()
    text = [
        f'Ехо у стані {hcode(state_name)}',
        'Зміст повідомлення:',
        hcode(message.text)
    ]
    await message.answer('\n'.join(text))

