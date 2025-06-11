import telebot
from telebot import types
from telebot import apihelper

TOKEN = 'token'
bot = telebot.TeleBot(TOKEN)

counters = {}

def increment_counter(button_name):
    if button_name in counters:
        counters[button_name] += 1
    else:
        counters[button_name] = 1

@bot.message_handler(commands=['start'])
def start(m):
    main_menu(m)

def main_menu(m):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ['🥗 Завтраки', '🍝 Обеды', '🍰 Десерты', '🍹 Напитки']
    keyboard.add(*[types.KeyboardButton(name) for name in buttons])
    bot.send_message(m.chat.id, "Выберите категорию рецептов:", reply_markup=keyboard)

@bot.message_handler(content_types=["text"])
def handle_text(m):
    text = m.text
    increment_counter(text)

    if text == '🥗 Завтраки':
        kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
        kb.add('🍳 Яичница с овощами', '🥞 Блины с мёдом', '🔙 Назад')
        bot.send_message(m.chat.id, "Выберите завтрак:", reply_markup=kb)

    elif text == '🍹 Напитки':
        kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
        kb.add('☕ Кофе по-восточному', '🍓 Смуси из ягод', '🔙 Назад')
        bot.send_message(m.chat.id, "Выберите напиток:", reply_markup=kb)

    elif text == '🍝 Обеды':
        kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
        kb.add('🥩 Стейк с картофелем', '🍜 Лапша с овощами', '🔙 Назад')
        bot.send_message(m.chat.id, "Выберите обед:", reply_markup=kb)

    elif text == '🍰 Десерты':
        kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
        kb.add('🍫 Брауни', '🍮 Крем-брюле', '🔙 Назад')
        bot.send_message(m.chat.id, "Выберите десерт:", reply_markup=kb)

    elif text == '🍳 Яичница с овощами':
        bot.send_message(m.chat.id, "Рецепт: обжарьте овощи и добавьте яйца. Подавайте горячим. 🔥")

    elif text == '🥞 Блины с мёдом':
        bot.send_message(m.chat.id, "Рецепт: замесите тесто, жарьте блины, подавайте с мёдом. 🍯")

    elif text == '☕ Кофе по-восточному':
        bot.send_message(m.chat.id, "Рецепт: варите кофе с сахаром и специями в турке. ☕")

    elif text == '🍓 Смуси из ягод':
        bot.send_message(m.chat.id, "Рецепт: взбейте в блендере ягоды, йогурт и мёд. 🍓")

    elif text == '🥩 Стейк с картофелем':
        bot.send_message(m.chat.id, "Рецепт: обжарьте стейк, подавайте с картофелем фри. 🥩")

    elif text == '🍜 Лапша с овощами':
        bot.send_message(m.chat.id, "Рецепт: сварите лапшу, обжарьте с овощами. 🥕")

    elif text == '🍫 Брауни':
        bot.send_message(m.chat.id, "Рецепт: растопите шоколад, добавьте муку, яйца и выпекайте. 🍫")

    elif text == '🍮 Крем-брюле':
        bot.send_message(m.chat.id, "Рецепт: взбейте сливки, яйца, сахар. Запеките и карамелизуйте. 🔥")

    elif text == '🔙 Назад':
        main_menu(m)

    else:
        bot.send_message(m.chat.id, f"Я не понял команду: {text}")

    count = counters.get(text, 0)
    bot.send_message(m.chat.id, f"Кнопка '{text}' была нажата {count} раз.")

bot.polling(none_stop=True)
