import telebot
from telebot import types
import requests
import xml.dom.minidom


TELEGRAM_TOKEN = 'token'
bot = telebot.TeleBot(TELEGRAM_TOKEN)

user_states = {}

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("USD", "EUR")
    msg = bot.send_message(message.chat.id, "Выбери валюту:", reply_markup=markup)
    bot.register_next_step_handler(msg, ask_date)

def ask_date(message):
    chat_id = message.chat.id
    user_states[chat_id] = {'currency': message.text}
    msg = bot.send_message(chat_id, "Введи дату в формате ДД/ММ/ГГГГ (например, 23/04/2025):")
    bot.register_next_step_handler(msg, get_currency_rate)

def get_currency_rate(message):
    chat_id = message.chat.id
    currency = user_states[chat_id]['currency']
    date = message.text.strip()

    # Формируем URL с датой
    url = f'https://cbr.ru/currency_base/daily/?UniDbQuery.Posted=True&UniDbQuery.To={date}'
    response = requests.get(url)

    if response.status_code != 200:
        bot.send_message(chat_id, "Ошибка при получении данных с сайта ЦБ.")
        return

    # Парсим HTML с помощью BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Ищем таблицу с курсами валют
    table = soup.find('table', {'class': 'data'})
    if not table:
        bot.send_message(chat_id, "Не удалось найти таблицу с курсами.")
        return

    # Ищем строки в таблице
    rows = table.find_all('tr')

    result = "Валюта не найдена."
    for row in rows[1:]:  # Пропускаем заголовок таблицы
        cols = row.find_all('td')
        if len(cols) > 4:  # Если в строке достаточно столбцов
            char_code = cols[1].text.strip()
            value = cols[4].text.strip()

            if char_code == currency:
                result = f"Курс {char_code} на {date} — {float(value):.4f} руб."
                break

    bot.send_message(chat_id, result)

bot.polling()
