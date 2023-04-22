import telebot
import config
from flask import Flask, request

#Initiate bot instance and webhook
bot = telebot.TeleBot(config.API_TOKEN)
server = Flask(__name__)


#At flask
@server.route('/', methods=['GET', 'HEAD'])
def index():
    return 'Blocknexus Bot active!', 200

@server.route('/' + config.API_TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200
#tele webhook config
bot.remove_webhook()
bot.set_webhook(url='https://fqfmrvssaa7wf6hg7t3fypz6dq.srv.us/' + config.API_TOKEN)
#server
server.run(port=8000, debug=True)