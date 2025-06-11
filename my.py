import telebot
import requests

TELEGRAM_TOKEN = '7967836998:AAH0ow-VyC6cIkrL35WK6rXlrK-AWrTob1c'
VK_TOKEN = 'vk1.a.eaHoUENp7_DMHLEAtq6xM5bTgxHUcg5vYb_YfJvYhMeX5hRNmYz5aNRdtd6zYps5YqSOtvNKEe3JO8N2T9kkMR2Mv2IjBD4ltUxjgBjVRk6lpCgALtXFt8D4Y4ZqfPgIOejbBtKWBmPqj2jOFweK-Y70tA-Omf3i9XzwVR1VFjPxF-2PvFqxntqehNvNqUUVDMAxrU9mkKxF33s8I2LAzw'
VK_USER_ID = '593760956'  

bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(content_types=['text'])
def handle_message(message):
    user = message.from_user.first_name
    text = message.text
    comment_text = f"Сообщение из Telegram от {user}: {text}"

    wall_get_url = 'https://api.vk.com/method/wall.get'
    wall_params = {
        'access_token': VK_TOKEN,
        'v': '5.131',
        'owner_id': VK_USER_ID,
        'count': 1
    }
    response = requests.get(wall_get_url, params=wall_params)
    if response.status_code != 200:
        bot.reply_to(message, "Ошибка при получении поста ВК.")
        return

    data = response.json()
    if 'error' in data:
        bot.reply_to(message, f"Ошибка ВК: {data['error']['error_msg']}")
        return

    try:
        post_id = data['response']['items'][0]['id']
    except (KeyError, IndexError):
        bot.reply_to(message, "Не найден последний пост для комментирования.")
        return

    # === Отправляем комментарий ===
    comment_url = 'https://api.vk.com/method/wall.createComment'
    comment_params = {
        'access_token': VK_TOKEN,
        'v': '5.131',
        'owner_id': VK_USER_ID,
        'post_id': post_id,
        'message': comment_text
    }
    comment_response = requests.get(comment_url, params=comment_params)
    result = comment_response.json()

    if 'response' in result:
        bot.reply_to(message, "")
    else:
        error = result.get('error', {}).get('error_msg', 'Неизвестная ошибка')
        bot.reply_to(message, f"Ошибка при комментировании: {error}")

bot.polling()
