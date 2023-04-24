from telebot.types import ReplyKeyboardMarkup, KeyboardButton

def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn_exch = KeyboardButton("Start Exchange 💱")
    btn_curate = KeyboardButton("Currency Rates ₿")
    btn_ordhist = KeyboardButton("Exchange History 🧾")
    btn_guide = KeyboardButton("Bot Guide 📗")
    btn_support = KeyboardButton("Open Ticket 🔖")
    markup.add(btn_exch, btn_curate, btn_ordhist, btn_guide, btn_support)
    return markup