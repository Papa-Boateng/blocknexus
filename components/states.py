from telebot.handler_backends import State, StatesGroup

class NexusSection(StatesGroup):
    exchange_state = State()
    currency_rt_state = State()
    tickets_state = State()