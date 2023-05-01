import config
from components import block_msg, keyboard, states, db, coinbase_client, payment_address
import telebot
from telebot import custom_filters
from telebot.storage import StateMemoryStorage
from flask import Flask, request
import coinaddrvalidator
from firebase_admin import firestore

#State Storage
state_storage = StateMemoryStorage()
#Initiate bot instance and webhook
bot = telebot.TeleBot(config.API_TOKEN, state_storage=state_storage, parse_mode='html')
server = Flask(__name__)
#initialize coinbase
cb_client = coinbase_client.cb_client_init

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

#############COMMANDS
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
        set_users_db = db.new_db.collection('users')
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
                'pay_to_address': [],
                'send_to_address': [],
                'date_joined': firestore.SERVER_TIMESTAMP
            })
    except Exception as e:
        send_error_message(chat_id, e)

@bot.message_handler(commands=['start_exchange'])
def start_exchange(message):
    try:
        chat_id=message.chat.id
        msg=("<b>BlockNexus Exchange</b> 💱\n\n"
             "To begin, you must enter the amount to exchange from\n"
             "the base currency is BTC(USD)\n\n"
             "<em>Enter <b>Amount</b> and select options from below</em>")
        bot.send_message(chat_id=chat_id, text=msg, reply_markup=keyboard.start_exchange_amount())
        bot.set_state(message.from_user.id, states.NexusSection.exchange_state, chat_id)
    except Exception as e:
        send_error_message(chat_id, e)
################

#Menu Keyboard Functions
@bot.message_handler(func=lambda message: message.text=='Start Exchange 💱')
def menu_itm_st(message):
    try:
        chat_id=message.chat.id
        msg=("<b>BlockNexus Exchange</b> 💱\n\n"
             "To begin, you must enter the amount to exchange from\n"
             "the base currency is BTC(USD)\n\n"
             "<em>Enter <b>Amount</b> and select options from below</em>")
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
            bot.set_state(message.from_user.id, states.ExchangeState.currency_from, chat_id)
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
@bot.message_handler(state=states.ExchangeState.currency_from)
def from_currency(message):
    try:
        chat_id=message.chat.id
        global enable_currency_convert
        value_type = message.text
        if value_type == 'BTC ₿':
            enable_currency_convert = "BTC"
            bot.send_message(chat_id=chat_id, text="Confirm <b>BTC</b> or change currency", reply_markup=keyboard.supported_currency())
            bot.set_state(message.from_user.id, states.ExchangeState.currency_to, chat_id)
            ##set state currency to
        elif value_type == 'USD $':
            enable_currency_convert = "USD"
            bot.send_message(chat_id=chat_id, text="Select the crypto currency to be equivalent in USD", reply_markup=keyboard.supported_currency())
            bot.set_state(message.from_user.id, states.ExchangeState.currency_to, chat_id)
            ##Set state currency to
        elif value_type == '⇦':
            bot.delete_state(message.from_user.id, chat_id)
            bot.send_message(chat_id=chat_id, text="⇦Back to <b>Dashboard</b>", reply_markup=keyboard.main_menu())
        else:
            bot.send_message(chat_id=chat_id, text="<code>invalid option</code>")
    except Exception as e:
        send_error_message(chat_id, e)

#currency to
@bot.message_handler(state=states.ExchangeState.currency_to)
def to_currency(message):
    try:
        chat_id=message.chat.id
        _from_convert_currency = message.text
        if _from_convert_currency in config.currency:
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                base_amount = float(data['amount'])
                if enable_currency_convert == 'USD':
                    current_price = cb_client.get_exchange_rates(currency=_from_convert_currency)
                    _in_usd = float(current_price['rates']['USD'])
                    _in_crypto = base_amount/_in_usd
                    crypto_amount = '{:0.8f}'.format(_in_crypto)
                    msg = block_msg.currency_from_msg.format(_from_convert_currency, crypto_amount, '{:0,.2f}'.format(base_amount))
                    data['usd_amount'] = base_amount
                    data['crypto_amount'] = crypto_amount
                elif enable_currency_convert == 'BTC':
                    current_price = cb_client.get_exchange_rates(currency=_from_convert_currency)
                    _in_usd = base_amount*float(current_price['rates']['USD'])
                    msg = block_msg.currency_from_msg.format(_from_convert_currency, '{:0.8f}'.format(base_amount), '{:0,.2f}'.format(_in_usd))
                    data['usd_amount'] = _in_usd
                    data['crypto_amount'] = base_amount
                bot.send_message(chat_id=chat_id, text=msg)
            bot.set_state(message.from_user.id, states.ExchangeState.currency_address, chat_id)
        elif _from_convert_currency == '⇦':
            bot.send_message(chat_id=chat_id, text="⇦Back to <b>amount in USD/BTC</b> select", reply_markup=keyboard.start_exchange_amount())
            bot.set_state(message.from_user.id, states.ExchangeState.currency_from, chat_id)
        else:
            bot.send_message(chat_id=chat_id, text="<code>Invalid entry</code>")
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['from_currency'] = _from_convert_currency
    except Exception as e:
        send_error_message(chat_id, e)

#currency address
@bot.message_handler(state=states.ExchangeState.currency_address)
def currency_address(message):
    try:
        chat_id=message.chat.id
        _to_convert_currency = message.text
        
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            msg = block_msg.currency_to_msg.format(data['from_currency'],_to_convert_currency, '{:0.8f}'.format(float(data['crypto_amount'])), '{:0,.2f}'.format(float(data['usd_amount'])) )
            bot.send_message(chat_id=chat_id, text=msg)
        if _to_convert_currency in config.currency and _to_convert_currency != data['from_currency']:
            bot.set_state(message.from_user.id, states.ExchangeState.exchange_review, chat_id)
            nw_msg = (f"Now Enter your <b>{_to_convert_currency}</b> address\n"
                      "to receive the exchanged currency.")
            bot.send_message(chat_id=chat_id, text=nw_msg, reply_markup=keyboard.return_kb())
        elif _to_convert_currency in config.currency and _to_convert_currency == data['from_currency']:
            bot.send_message(chat_id=chat_id, text="<code>Cannot convert to the same currency</code>")
        elif _to_convert_currency == '⇦':
            bot.send_message(chat_id=chat_id, text="⇦Back to <b>Currency from</b> exchange", reply_markup=keyboard.supported_currency())
            bot.set_state(message.from_user.id, states.ExchangeState.currency_to, chat_id)
        else:
            bot.send_message(chat_id=chat_id, text="<code>Invalid entry</code>")
        print(data['from_currency'])
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['to_currency'] = _to_convert_currency
    except Exception as e:
        send_error_message(chat_id, e)

#currency review
@bot.message_handler(state=states.ExchangeState.exchange_review)
def exchange_review(message):
    try:
        chat_id=message.chat.id
        global order
        _currency_address = message.text
        if _currency_address == '⇦':
            bot.send_message(chat_id=chat_id, text="⇦Back to <b>Currency from</b> exchange", reply_markup=keyboard.supported_currency())
            bot.set_state(message.from_user.id, states.ExchangeState.currency_to, chat_id)
        else:
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                valid_address = coinaddrvalidator.validate(data['to_currency'].lower(), _currency_address)
                if valid_address.valid == True:
                    msg = block_msg.currency_review.format(data['from_currency'],data['to_currency'], '{:0.8f}'.format(float(data['crypto_amount'])), '{:0,.2f}'.format(float(data['usd_amount'])), _currency_address)
                    bot.send_message(chat_id=chat_id, text=msg, reply_markup=keyboard.confirm_kb())
                    bot.set_state(message.from_user.id, states.ExchangeState.exchange_confirm, chat_id)
                    order = {'currency_from': data['from_currency'],
                             'currency_to': data['to_currency'],
                             'crypto_amount': data['crypto_amount'],
                             'usd_amount': data['usd_amount'],
                             'recieve_address': _currency_address}        
                else:
                    bot.send_message(chat_id=chat_id, text=f"<code>Enter a valid {data['to_currency']} address</code>")
    except Exception as e:
        send_error_message(chat_id, e)
#currency confirm
@bot.message_handler(state=states.ExchangeState.exchange_confirm)
def exchange_confirm(message):
    try:
        chat_id=message.chat.id
        select_option = message.text
        set_users_db = db.new_db.collection('users')
        time_new = '00:30:00'
        if select_option == 'Confirm ✅':
            bot.send_message(chat_id=chat_id, text="<em>processing...</em>")
            payment_address.process_new_address(chat_id, order['currency_from'], message)
            _user_valid_address = set_users_db.document(str(chat_id)).get()
            get_user_data = _user_valid_address.to_dict()
            send_to_address = get_user_data['pay_to_address'][0]
            msg = block_msg.exchange_confirm_msg.format(order['currency_from'], order['currency_to'], '{:0.8f}'.format(float(order['crypto_amount'])), '{:0,.2f}'.format(float(order['usd_amount'])), order['recieve_address'], order['currency_from'], send_to_address, '{:0.8f}'.format(float(order['crypto_amount'])), time_new)
            bot.send_message(chat_id=chat_id, text=msg, reply_markup=keyboard.done_action_kb())
        elif select_option == '⇦':
            bot.set_state(message.from_user.id, states.ExchangeState.exchange_review, chat_id)
            bot.send_message(chat_id=chat_id, text="Re-enter Receive address", reply_markup=keyboard.return_kb())
        elif select_option == 'Done ✅':
            bot.delete_state(message.from_user.id, chat_id)
            bot.send_message(chat_id=chat_id, text="<b>Dashboard</b>", reply_markup=keyboard.main_menu())
        else:
            bot.send_message(chat_id=chat_id, text="Choose from menu")
    except Exception as e:
        send_error_message(chat_id, e)
#Process completed



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