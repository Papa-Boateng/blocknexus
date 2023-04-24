import config
from components import block_msg, keyboard, states
import telebot
from telebot.storage import StateMemoryStorage
from flask import Flask, request
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

#State Storage
state_storage = StateMemoryStorage()
#Initiate bot instance and webhook
bot = telebot.TeleBot(config.API_TOKEN, state_storage=state_storage, parse_mode='html')
server = Flask(__name__)
#FireStore instance
cred = credentials.Certificate("auth/serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()


#To restart/start bot
@bot.message_handler(commands=['start'])
def start_bot(message):
    try:
        chat_id = message.chat.id
        username = message.from_user.username
        f_name = message.from_user.first_name
        l_name = message.from_user.last_name
        call_full_name = f"{f_name} {l_name}"
        set_users_db = db.collection('users')
        query_db = set_users_db.document(str(chat_id))
        query_res = query_db.get()
        if query_res.exists:
            msg = block_msg.exist_user.format(call_full_name)
            bot.send_message(chat_id=chat_id, text=msg, reply_markup=keyboard.main_menu())
        else:
            msg = block_msg.new_user.format(call_full_name)
            bot.send_message(chat_id=chat_id, text=msg, reply_markup=keyboard.main_menu())
            query_db.set({
                'chat_id': chat_id,
                'first_name': f_name,
                'last_name': l_name,
                'username': username,
                'history': [],
                'tickets': {},
                'date_joined': firestore.SERVER_TIMESTAMP
            })
    except Exception as e:
        bot.send_message(chat_id, f'Error: {e}')


bot.enable_save_next_step_handlers(delay=1)
bot.load_next_step_handlers()

#At flask --APP FOOTER
@server.route('/', methods=['GET', 'HEAD'])
def index():
    return 'Blocknexus Bot active!', 200

@server.route('/' + config.API_TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200
#webhook config
config.Webhook()
#server
server.run(port=8000, debug=True)