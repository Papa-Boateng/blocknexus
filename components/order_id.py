import random
import string
from components import db

#Set db
get_users = db.new_db.collection('users')

def process_order_id(length):
    return ''.join(
        random.choices(
            string.ascii_letters + string.digits,
            k=length
        )
    )


def process_order_history(chat_id, orders):
    select_user_info = get_users.document(str(chat_id))
    read_user_info = select_user_info.get()
    get_user_data = read_user_info.to_dict()
    order_history = get_user_data['history']
    order_history.append(orders)
    select_user_info.update({
        'history': order_history
    })
    