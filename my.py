from telebot import TeleBot, types

bot = TeleBot("token")

# reply-кнопки (из лабораторной 8)
@bot.message_handler(commands=['start'])
def start(message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("📋 Меню рецептов", "ℹ️ О боте")
    bot.send_message(message.chat.id, "Привет! Выбери опцию:", reply_markup=kb)

# обработка обычных reply-кнопок
@bot.message_handler(func=lambda msg: msg.text == "📋 Меню рецептов")
def show_inline_menu(message):
    inline_kb = types.InlineKeyboardMarkup()
    inline_kb.add(types.InlineKeyboardButton("🍝 Итальянская", callback_data="italian"))
    inline_kb.add(types.InlineKeyboardButton("🍣 Японская", callback_data="japanese"))
    inline_kb.add(types.InlineKeyboardButton("🌮 Мексиканская", callback_data="mexican"))
    inline_kb.add(types.InlineKeyboardButton("🍰 Десерты", callback_data="desserts"))
    bot.send_message(message.chat.id, "Выберите категорию:", reply_markup=inline_kb)

@bot.message_handler(func=lambda msg: msg.text == "ℹ️ О боте")
def about(message):
    bot.send_message(message.chat.id, "Этот бот поможет выбрать и посмотреть рецепты популярных блюд.")

# обработка inline-кнопок
@bot.callback_query_handler(func=lambda call: True)
def handle_inline_menu(call):
    submenu = types.InlineKeyboardMarkup()
    
    if call.data == "italian":
        submenu.add(types.InlineKeyboardButton("Паста", callback_data="carbonara"))
        submenu.add(types.InlineKeyboardButton("Пицца", callback_data="margherita"))
        bot.edit_message_text("Выберите блюдо из итальянской кухни:", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=submenu)
    
    elif call.data == "japanese":
        submenu.add(types.InlineKeyboardButton("Суши", callback_data="sushi"))
        submenu.add(types.InlineKeyboardButton("Рамен", callback_data="ramen"))
        bot.edit_message_text("Выберите блюдо из японской кухни:", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=submenu)

    elif call.data == "mexican":
        submenu.add(types.InlineKeyboardButton("Тако", callback_data="taco"))
        submenu.add(types.InlineKeyboardButton("Буррито", callback_data="burrito"))
        bot.edit_message_text("Выберите блюдо из мексиканской кухни:", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=submenu)

    elif call.data == "desserts":
        submenu.add(types.InlineKeyboardButton("Тирамису", callback_data="tiramisu"))
        submenu.add(types.InlineKeyboardButton("Чизкейк", callback_data="cheesecake"))
        bot.edit_message_text("Выберите десерт:", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=submenu)

    else:
        # финальный ответ — рецепт или описание
        recipes = {
            "carbonara": "🍝 Паста Карбонара: яйца, бекон, пармезан, спагетти.",
            "margherita": "🍕 Пицца Маргарита: томаты, моцарелла, базилик.",
            "sushi": "🍣 Суши: рис, рыба, нори, васаби.",
            "ramen": "🍜 Рамен: лапша, бульон, мясо, яйца, овощи.",
            "taco": "🌮 Тако: лепёшка, мясо, овощи, соус.",
            "burrito": "🌯 Буррито: лепёшка, рис, фасоль, мясо, сыр.",
            "tiramisu": "🍰 Тирамису: печенье савоярди, кофе, маскарпоне, какао.",
            "cheesecake": "🍰 Чизкейк: сливочный сыр, печенье, сахар, ваниль."
        }
        text = recipes.get(call.data, "Рецепт не найден.")
        bot.send_message(call.message.chat.id, text)

bot.polling(none_stop=True)
