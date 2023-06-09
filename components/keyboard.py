from config import currency
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

#menu kb
def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn_exch = KeyboardButton("Start Exchange 💱")
    btn_curate = KeyboardButton("Currency Rates ₿")
    btn_ordhist = KeyboardButton("Exchange History 🧾")
    btn_guide = KeyboardButton("Bot Guide 📗")
    btn_support = KeyboardButton("Open Ticket 🔖")
    markup.add(btn_exch, btn_curate, btn_ordhist, btn_guide, btn_support)
    return markup

#Inner Menu kb

#Confirm
def confirm_kb():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row_width = 1
    btn_ok = KeyboardButton("Confirm ✅")
    btn_return = KeyboardButton("⇦")
    markup.add(btn_ok,btn_return)
    return markup
#return btn
def return_kb():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn_return = KeyboardButton("⇦")
    markup.add(btn_return)
    return markup

def done_action_kb():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn_return = KeyboardButton("Done ✅")
    markup.add(btn_return)
    return markup
#start exchange
def start_exchange_amount():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn_usd = KeyboardButton("USD $")
    btn_btc = KeyboardButton("BTC ₿")
    btn_return = KeyboardButton("⇦")
    markup.add(btn_usd,btn_btc)
    markup.add(btn_return)
    return markup

#Currency Kb
def supported_currency():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    #markup.row_width = 2
    for coin in currency:
        markup.add(KeyboardButton(coin))
    markup.add(KeyboardButton('⇦'))
    return markup

