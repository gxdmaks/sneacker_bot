from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


def main_menu_kb(products_from_db):
    kb = InlineKeyboardMarkup(row_width=2)
    order = InlineKeyboardButton(text='Оформить заказ',callback_data='order')
    cart = InlineKeyboardButton(text='Корзина',callback_data='cart')
    all_products = [InlineKeyboardButton(text=i[0],callback_data=i[1])
                    for i in products_from_db]
    kb.row(order)
    kb.add(*all_products)
    kb.row(cart)
    return kb

def choose_product_count(plus_or_minus='',current_amount=1):
    kb = InlineKeyboardMarkup(row_width=3)
    back = InlineKeyboardButton(text='Назад',callback_data='back')
    plus = InlineKeyboardButton(text='+',callback_data='increment')
    minus = InlineKeyboardButton(text='-',callback_data='decrement')
    count = InlineKeyboardButton(text=str(current_amount),
                                 callback_data=str(current_amount))
    add_to_cart = InlineKeyboardButton(text='Добавить в корзину',callback_data='add_to_cart')

    if plus_or_minus == 'increment':
        new_amount = int(current_amount)+1
        count = InlineKeyboardButton(text=str(new_amount),
                                     callback_data=str(new_amount))

    elif plus_or_minus == 'decrement':
        if int(current_amount) > 1:
            new_amount = int(current_amount)-1
            count = InlineKeyboardButton(text=str(new_amount),
                                         callback_data=str(new_amount))

    kb.add(minus,count,plus)
    kb.row(add_to_cart)
    kb.row(back)
    return kb

def phone_number_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    number = KeyboardButton('Поделится контактом', request_contact=True)
    kb.add(number)

    return kb

def location_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    location = KeyboardButton('Поделится локацией', request_location=True)
    kb.add(location)

    return kb

def get_accept_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)

    yes = KeyboardButton('Подтвердить')
    no = KeyboardButton('Отменить')
    kb.add(yes,no)

    return kb

def get_cart_kb():
    kb = InlineKeyboardMarkup(row_width=1)

    clear_cart = InlineKeyboardButton('Очистить корзину',callback_data='clear_cart')
    order = InlineKeyboardButton('Оформить заказ',callback_data='order')
    back = InlineKeyboardButton('Назад',callback_data='back')

    kb.add(clear_cart,order,back)

    return kb
