import asyncio
import random
from datetime import datetime
import pytz

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = "8524038504:AAFwLug-98RMALtoqHd04CrojBIVlbV7Ql4"  # ЗАМЕНИТЕ НА СВОЙ ТОКЕН!

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Команды
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет! Я твой первый бот на aiogram! Используй /help для списка команд")

@dp.message(Command("hi"))
async def cmd_hi(message: types.Message):
    await message.answer("Привет! Бро 👋")

@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    help_text = """
📚 Доступные команды:
/start - Начать работу
/hi - Поприветствовать
/help - Справка
/time - Текущее время
/random - Случайное число
/menu - Меню с кнопками
/about - О боте
/inline - Inline-кнопки
    """
    await message.answer(help_text)

@dp.message(Command("about"))
async def cmd_about(message: types.Message):
    await message.answer("🤖 Мой первый Telegram-бот\nВерсия: 1.0\nСоздан с помощью aiogram 3.x")

@dp.message(Command("time"))
async def cmd_time(message: types.Message):
    from datetime import datetime, timedelta
    
    # UTC время
    utc_now = datetime.utcnow()
    
    # Добавляем 3 часа для Москвы (летнее/зимнее время не учитывается)
    moscow_time = utc_now + timedelta(hours=3)
    
    current_time = moscow_time.strftime("%H:%M:%S")
    await message.answer(f"🕐 Время UTC+3: {current_time}\n(UTC было: {utc_now.strftime('%H:%M:%S')})")

@dp.message(Command("random"))
async def cmd_random(message: types.Message):
    number = random.randint(1, 100)
    await message.answer(f"🎲 Случайное число: {number}")

# Меню с кнопками
@dp.message(Command("menu"))
async def cmd_menu(message: types.Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Привет 👋"), KeyboardButton(text="Время 🕐")],
            [KeyboardButton(text="Случайное число 🎲"), KeyboardButton(text="Помощь ❓")]
        ],
        resize_keyboard=True
    )
    await message.answer("Выберите действие:", reply_markup=keyboard)

# Обработка кнопок меню
@dp.message(lambda message: message.text == "Привет 👋")
async def handle_hi_button(message: types.Message):
    await message.answer("И тебе привет! 😊")

@dp.message(lambda message: message.text == "Время 🕐")
async def handle_time_button(message: types.Message):
    from datetime import datetime, timedelta
    
    # UTC время
    utc_now = datetime.utcnow()
    
    # Добавляем 3 часа для Москвы (летнее/зимнее время не учитывается)
    moscow_time = utc_now + timedelta(hours=3)
    
    current_time = moscow_time.strftime("%H:%M:%S")
    await message.answer(f"🕐 Время UTC+3: {current_time}\n(UTC было: {utc_now.strftime('%H:%M:%S')})")

@dp.message(lambda message: message.text == "Случайное число 🎲")
async def handle_random_button(message: types.Message):
    number = random.randint(1, 100)
    await message.answer(f"🎲 Ваше число: {number}")

@dp.message(lambda message: message.text == "Помощь ❓")
async def handle_help_button(message: types.Message):
    help_text = """
📚 Доступные команды:
/start - Начать работу
/hi - Поприветствовать
/help - Справка
/time - Текущее время
/random - Случайное число
/menu - Меню с кнопками
/about - О боте
/inline - Inline-кнопки

📱 Или используйте кнопки меню!
    """
    await message.answer(help_text)

# Inline-кнопки
@dp.message(Command("inline"))
async def cmd_inline(message: types.Message):
    inline_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="👍 Нравится", callback_data="like"),
             InlineKeyboardButton(text="👎 Не нравится", callback_data="dislike")],
            [InlineKeyboardButton(text="Открыть GitHub", url="https://github.com")]
        ]
    )
    await message.answer("Как вам этот бот?", reply_markup=inline_kb)

@dp.callback_query(lambda c: c.data in ["like", "dislike"])
async def process_callback(callback_query: types.CallbackQuery):
    if callback_query.data == "like":
        await callback_query.answer("Спасибо за лайк! ❤️")
        await callback_query.message.answer("Вы поставили лайк!")
    else:
        await callback_query.answer("Попробуем улучшить бота! 🤝")

# Обработка любых других сообщений
@dp.message()
async def handle_other_messages(message: types.Message):
    # Убираем клавиатуру меню, если пользователь написал текст
    await message.answer("Используйте /menu для открытия меню или /help для списка команд")

# Запуск
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())