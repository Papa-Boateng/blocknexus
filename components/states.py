from telebot.handler_backends import State, StatesGroup

class NexusSection(StatesGroup):
    exchange_state = State()
    currency_rt_state = State()
    tickets_state = State()
    base = State()

class ExchangeState(StatesGroup):
    currency_from = State()
    currency_to = State()
    currency_address = State()
    exchange_review = State()
    exchange_confirm = State()