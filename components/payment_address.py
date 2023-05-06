import config
import telebot
import qrcode
import time
from components import coinbase_client, db
#Initiate bot instance and webhook
bot = telebot.TeleBot(config.API_TOKEN, parse_mode='html')

#Set db
get_users = db.new_db.collection('users')

cb_client = coinbase_client.cb_client_init

def process_new_address(chat_id, deposit_curreny, message):
    pay_to_account = coinbase_client.type_payment(deposit_curreny)
    select_account = cb_client.get_account(pay_to_account)
    select_user_info = get_users.document(str(chat_id))
    read_user_info = select_user_info.get()
    get_user_data = read_user_info.to_dict()
    payment_address = get_user_data['pay_to_address']
    #_usr_activity = get_user_data['user_activity']
    account_address = select_account.create_address() 
    label = account_address['address_label'] 
    tool_tip = label.split()
    _network = account_address['network']
    _delimiter = len(_network)
    network = _network[0].upper()+ _network[1:_delimiter]
    #title =  "{} ({})".format(network, tool_tip[0])  
    address = account_address['address']
    qr = qrcode.make(address)
    qr_code_img = qr.get_image()
    time.sleep(0.5)
    bot.delete_message(chat_id=chat_id, message_id=message.message_id+1)
    bot.send_photo(chat_id, qr_code_img, caption=address)
    time.sleep(0.5)
    bot.send_message(chat_id=chat_id, text=f'Pay <b>only {deposit_curreny}</b> to this Address. <b>Do not send</b> any other than {deposit_curreny}')
    payment_address.append(address)
    select_user_info.update({
        'pay_to_address': payment_address
    }) 
    time.sleep(0.5)