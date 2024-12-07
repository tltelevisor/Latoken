import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from oai import oai_context, collect_mess, oai_fact, oai_give_question, oai_check_answer
from config import BOT_TOKEN
logging.basicConfig(level=logging.INFO, filename='latoken.log',
                    format='%(asctime)s %(levelname)s %(message)s')

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

kb = [
    [
        types.KeyboardButton(text="Расскажи факт о LATOKEN"),
        types.KeyboardButton(text="Задай вопрос")
    ],
]
keyboard = types.ReplyKeyboardMarkup(
    keyboard=kb,
    resize_keyboard=True
)

user_data = {}

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    if message.from_user in user_data:
        del user_data[message.from_user]
    name = f'{message.from_user.full_name} ({message.from_user.username})'
    await message.answer(f'Привет, {name}! Спроси о LATOKEN!', reply_markup=keyboard)


@dp.message(Command("menu"))
async def cmd_start(message: types.Message):
    if message.from_user in user_data:
        del user_data[message.from_user]
    await message.answer(f'Спроси о LATOKEN или проверь себя, получив вопрос', reply_markup=keyboard)


@dp.message(F.text == "Расскажи факт о LATOKEN")
async def facts(message: types.Message):
    if message.from_user in user_data:
        del user_data[message.from_user]
    fact = oai_fact(message.from_user)
    await message.reply(fact)

@dp.message(F.text == "Задай вопрос")
async def check(message: types.Message):
    question = oai_give_question(message.from_user)
    user_data[message.from_user] = question
    await message.reply(question)

@dp.message()
async def oai_answer(message: types.Message):
    if message.from_user not in user_data:
        messages = collect_mess(message.from_user, message.text)
        oai_answer = oai_context(message.from_user, messages)
    else:
        oai_answer = oai_check_answer(message.from_user, user_data[message.from_user], message.text)
        del user_data[message.from_user]
    # oai_answer = oai_no_context(msg.from_user, messages)
    await message.answer(f'{oai_answer}')

async def main():
    print("Start bot")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())