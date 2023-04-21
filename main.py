import telebot
import config
from flask import Flask, request

#Initiate bot instance and webhook
bot = telebot.TeleBot(config.API_TOKEN)
server = Flask(__name__)


#bot. infinity_polling()
@server.route('/' + config.API_TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200
