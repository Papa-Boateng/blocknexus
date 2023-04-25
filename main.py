import config
from components import block_msg, keyboard, states
import telebot
from telebot import custom_filters
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


#Handlers

#ERROR HANDLER MSG
def send_error_message(chat_id, e):
    bot.send_message(chat_id, f'Error: {e}')
#Float message handler
def input_float_parser(s):
    try:
        float(s)
        return True
    except:
        return False


#To restart/start bot
@bot.message_handler(commands=['start'])
def start_bot(message):
    try:
        chat_id = message.chat.id
        bot.set_state(message.from_user.id, states.NexusSection.base, chat_id)
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
        send_error_message(chat_id, e)

#Menu Keyboard Functions
@bot.message_handler(func=lambda message: message.text=='Start Exchange 💱')
def menu_itm_st(message):
    try:
        chat_id=message.chat.id
        msg=("<b>BlockNexus Exchange</b> 💱\n\n"
             "To begin, you must enter the amount to exchange from\n"
             "the base currency is BTC(USD)\n\n"
             "<em>Enter amound and select Options from below</em>")
        bot.send_message(chat_id=chat_id, text=msg, reply_markup=keyboard.start_exchange_amount())
        bot.set_state(message.from_user.id, states.NexusSection.exchange_state, chat_id)
    except Exception as e:
        send_error_message(chat_id, e)

#States
#Start Exchange State
@bot.message_handler(state=states.NexusSection.exchange_state)
def exchange_amount(message):
    try:
        chat_id=message.chat.id
        amount = message.text
        test_digi = amount.isdigit()
        test_deci = input_float_parser(amount)
        if test_digi or test_deci:
            bot.send_message(chat_id=chat_id, text="Now select from below whether amount is in 'USD' or 'BTC'")
            bot.set_state(message.from_user.id, states.ExhangeState.currency_from, chat_id)
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data['amount'] = amount
        elif amount == '⇦':
            bot.delete_state(message.from_user.id, chat_id)
            bot.send_message(chat_id=chat_id, text="⇦Back to <b>Dashboard</b>", reply_markup=keyboard.main_menu())
        else:
            bot.send_message(chat_id=chat_id, text="<code>Enter numbers or decimals only</code>")
    except Exception as e:
        send_error_message(chat_id, e)
#currency from
@bot.message_handler(state=states.ExhangeState.currency_from)
def from_currency(message):
    try:
        chat_id=message.chat.id
        value_type = message.text
        if value_type == 'BTC':
            bot.send_message(chat_id=chat_id, text="Confirm <b>BTC</b> or change currency", reply_markup=keyboard.supported_currency())
            ##set state currency to
        elif value_type == 'USD':
            bot.send_message(chat_id=chat_id, text="Select the currency to be equivalent in USD", reply_markup=keyboard.supported_currency())
            ##Set state currency to
        elif value_type == '⇦':
            bot.delete_state(message.from_user.id, chat_id)
            bot.send_message(chat_id=chat_id, text="⇦Back to <b>Dashboard</b>", reply_markup=keyboard.main_menu())
        else:
            bot.send_message(chat_id=chat_id, text="<code>invalid option</code>")
    except Exception as e:
        send_error_message(chat_id, e)


bot.add_custom_filter(custom_filters.StateFilter(bot))

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