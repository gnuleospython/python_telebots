from telebot import TeleBot

TOKEN_BOT = '7217016747:AAF8wwtKCFcKFuO7DknBd1wyl8DLJ0EP-6w'

bot = TeleBot(TOKEN_BOT)

@bot.message_handler(commands=['start'])
def start(mensage):
    print("Entro al start del bot")
    bot.send_message("Bienvenido al SPA de Jazmin enque le podemos ayudar:")
    bot.register_next_step_handler(mensage)


if __name__ == '__main__':
    print("Esta ejecutandose el bot")
    bot.infinity_polling()
    