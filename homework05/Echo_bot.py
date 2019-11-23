import telebot


access_token = '1047250309:AAHfAz7XRhSY2Z13-wS2sXYm09wv2M0PNmM'
telebot.apihelper.proxy = {'https': 'https://91.236.239.149:3128'}

# Создание бота с указанным токеном доступа
bot = telebot.TeleBot(access_token)


# Бот будет отвечать только на текстовые сообщения
@bot.message_handler(content_types=['text'])
def echo(message: str) -> None:
    bot.send_message(message.chat.id, message.text)


if __name__ == '__main__':
    bot.polling()
