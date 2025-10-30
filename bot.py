import telebot
from datetime import datetime, date
import logging
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = "8196785015:AAFaq-VKk_ayjSnB95oxdoO8_kB1ZmlPLmE"
bot = telebot.TeleBot(BOT_TOKEN)

def create_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("2025-12-31"), KeyboardButton("2026-01-01"))
    keyboard.add(KeyboardButton("2025-04-02"), KeyboardButton("2026-03-11"))
    return keyboard

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = """
Привет!

Я помогу узнать, сколько дней осталось до любой даты или прошло с неё.

Просто отправь мне дату в формате:
- ГГГГ-ММ-ДД;
- ДД.ММ.ГГГГ.

Или выбери пример ниже 👇
    """
    bot.reply_to(message, welcome_text, reply_markup=create_keyboard())

@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = """
📖 Как пользоваться ботом:

Отправь сообщение с датой в одном из форматов:
- ГГГГ-ММ-ДД;
- ДД.ММ.ГГГГ.

Бот рассчитает разницу в днях между сегодняшней датой и указанной.
    """
    bot.reply_to(message, help_text)

def parse_date(date_str: str):
    date_formats = [
        '%Y-%m-%d',
        '%d.%m.%Y',
        '%d/%m/%Y',
    ]
    
    for fmt in date_formats:
        try:
            return datetime.strptime(date_str, fmt).date()
        except ValueError:
            continue
    return None

def calculate_days_difference(target_date: date):
    today = date.today()
    delta = (target_date - today).days
    
    if delta > 0:
        return f"📅 До {target_date} осталось {delta} дней 🎉"
    elif delta < 0:
        return f"📅 С {target_date} прошло {abs(delta)} дней ⏳"
    else:
        return f"🎊 Сегодня тот самый день — {target_date} 🎉"

@bot.message_handler(func=lambda message: True)
def handle_date(message):
    user_input = message.text.strip()
    
    print(f"Пользователь {message.from_user.first_name} отправил: {user_input}")
    
    target_date = parse_date(user_input)
    
    if target_date is None:
        error_text = "❌ Не могу распознать дату. Используй формат 2025-12-31 или 31.12.2025"
        bot.reply_to(message, error_text, reply_markup=create_keyboard())
        return
    
    result_text = calculate_days_difference(target_date)
    full_result = f"👤 Для: {message.from_user.first_name}\n{result_text}"
    
    bot.reply_to(message, full_result, reply_markup=create_keyboard())

def main():
    print("🔄 Запускаю бота...")
    
    if not BOT_TOKEN:
        print("❌ Ошибка: BOT_TOKEN не установлен!")
        return
    
    try:
        print("🤖 Бот запускается...")
        print("✅ Бот работает! Напиши /start в Telegram")
        bot.infinity_polling()
        
    except Exception as e:
        print(f"❌ Ошибка при запуске: {e}")

if __name__ == '__main__':
    main()