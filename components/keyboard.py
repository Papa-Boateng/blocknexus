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

#start exchange
def start_exchange_amount():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn_usd = KeyboardButton("USD")
    btn_btc = KeyboardButton("BTC")
    btn_return = KeyboardButton("⇦")
    markup.add(btn_usd,btn_btc)
    markup.add(btn_return)
    return markup

#Currency Kb
def supported_currency():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    for coin in currency:
        markup.add(KeyboardButton(coin))
    return markup