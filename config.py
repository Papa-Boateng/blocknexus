import telebot

API_TOKEN = "6235771664:AAGXSAtbqnieA6-8eXVUqrvpyWfrsBX3egM"

bot = telebot.TeleBot(API_TOKEN)

#BOT SUPPORTED CURRENCES
currency = ['BTC',
            'ETH',
            'LTC',
            'DASH']

#coinbase api
coinbase_api_key = 'w6FxDzDXrlRhDnlL'
coinbase_api_secret = 'ZrCcF1iH5oqrGU6XfTlSOWJWHwfyOh1g'


def Webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://fqfmrvssaa7wf6hg7t3fypz6dq.srv.us/' + API_TOKEN)
