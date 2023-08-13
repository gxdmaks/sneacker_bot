import database
import buttons
import telebot
from telebot.types import ReplyKeyboardRemove
from geopy.geocoders import Nominatim

bot = telebot.TeleBot('5956465222:AAFlR8RBtmGRXyjNJpExDn7l3Qq9PjiSlhs')
geolocator = Nominatim(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                  'Chrome/113.0.0.0 Safari/537.36')
users = {}

# database.add_to_cart('Air Jordan 1',60,100,'Air Jordan 1','https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.goat.com%2Fsneakers%2Fdior-x-air-jordan-1-high-dior-aj1-low&psig=AOvVaw2n1isw9hwJkbj4m8S2W1ga&ust=1686136055310000&source=images&cd=vfe&ved=0CBEQjRxqFwoTCODMzOPArv8CFQAAAAAdAAAAABAE')
# database.add_to_cart('Air Jordan 4',200,100,'Air Jordan 4','https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.highsnobiety.com%2Fp%2Fnike-air-jordan-4-military-black-release-info%2F&psig=AOvVaw3LFEwTb2nuHol9YmHz-lcR&ust=1686136173364000&source=images&cd=vfe&ved=0CBEQjRxqFwoTCNC4xPvArv8CFQAAAAAdAAAAABAE')
# обработка команды старт


@bot.message_handler(commands=['start'])

def start(message):
    user_id = message.from_user.id
    checker = database.check_user(user_id)
    if checker:
        products = database.get_product_name()
        bot.send_message(user_id,'привет',reply_markup=ReplyKeyboardRemove())
        bot.send_message(user_id, ' выберите пункт меню', reply_markup=buttons.main_menu_kb(products))
    elif not checker:
        bot.send_message(user_id, ' привет\nотправь имя')
        bot.register_next_step_handler(message, get_name)


@bot.message_handler(content_types=['text'])
def get_name(message):
    user_id = message.from_user.id
    name = message.text
    bot.send_message(user_id, 'отправь свой номер', reply_markup=buttons.phone_number_kb())
    bot.register_next_step_handler(message, get_number, name)


def get_number(message, name):
    user_id = message.from_user.id
    if message.contact:
        phone_number = message.contact.phone_number
        database.registration(user_id, name, phone_number, 'Not yet')
        products = database.get_product_name()
        bot.send_message(user_id,'привет',reply_markup=ReplyKeyboardRemove())
        bot.send_message(user_id, 'выберите пункт меню', reply_markup=buttons.main_menu_kb(products))
    elif not message.contact:
        bot.send_message(user_id, 'отправьте свой номер используя кнопку!', reply_markup=buttons.phone_number_kb())
        bot.register_next_step_handler(message, get_number, name)
@bot.callback_query_handler(lambda call: call.data in ['increment','decrement','add_to_cart','back'])
def get_user_product_count(call):
    user_id = call.message.chat.id
    if call.data == 'increment':
        actual_count = users[user_id]['pr_count']
        users[user_id]['pr_count'] += 1
        bot.edit_message_reply_markup(chat_id=user_id,
                                      message_id=call.message.message_id,
                                      reply_markup=buttons.choose_product_count('increment',actual_count))
    elif call.data == 'decrement':
        actual_count = users[user_id]['pr_count']
        users[user_id]['pr_count'] -= 1
        bot.edit_message_reply_markup(chat_id=user_id,
                                      message_id=call.message.message_id,
                                      reply_markup=buttons.choose_product_count('decrement',actual_count))
    elif call.data == 'back':
        products = database.get_product_name()
        bot.edit_message_text('Выберете пункт меню',
                              user_id
                              ,call.message.message_id,
                              reply_markup=buttons.main_menu_kb(products))

    elif call.data == 'add_to_cart':
        product_count = users[user_id]['pr_count']
        user_product = users[user_id]['pr_name']
        database.add_product_to_cart(user_id,user_product,product_count)
        products = database.get_product_name()
        bot.edit_message_text('Продукт добавлен в корзину',user_id,call.message.message_id,reply_markup=buttons.main_menu_kb(products))
@bot.callback_query_handler(lambda call: call.data in ['order','cart','clear_cart'])
def main_menu_handle(call):
    user_id = call.message.chat.id
    user_cart = database.get_exect_product_from_cart(user_id)
    message_id = call.message.message_id
    if call.data == 'order':
        bot.delete_message(user_id,message_id)
        bot.send_message(user_id,'Отправьте локацию',reply_markup=buttons.location_kb())
        bot.register_next_step_handler(call.message, get_location)
    elif call.data == 'cart':
        user_cart = database.get_exect_product_from_cart(user_id)
        full_text = 'Ваша корзина:\n\n'
        total_amount = 0
        for i in user_cart:
            full_text += f'{i[0]} x {i[1]} = {i[2]}\n'
            total_amount += i[2]

        full_text += f'\nИтог: {total_amount}'
        bot.edit_message_text(full_text,
                              user_id,
                              message_id,
                              reply_markup=buttons.get_cart_kb())

    elif call.data == 'clear_cart':
        database.delete_cart(user_id)
        bot.edit_message_text('Ваша корзина очищена',
                              user_id,
                              message_id,
                              reply_markup=buttons.main_menu_kb(database.get_product_name()))
def get_location(message):
    user_id = message.from_user.id
    if message.location:
        latitude = message.location.latitude
        longitude = message.location.longitude
        address = geolocator.reverse((latitude,longitude))
        user_cart = database.get_exect_product_from_cart(user_id)
        full_text = 'Ваш заказ:\n\n'
        user_info = database.get_user_number_name(user_id)
        full_text += f'Имя: {user_info[0]}\nНомер телефона: {user_info[1]}\n\n'
        total_amount = 0
        for i in user_cart:
            full_text += f'{i[0]} x {i[1]} = {i[2]}\n'
            total_amount += i[2]

        full_text+=f'\nИтог: {total_amount}\nАдрес: {address}'
        bot.send_message(user_id,full_text,reply_markup=buttons.get_accept_kb())
        bot.register_next_step_handler(message,get_accept, address,full_text)
def get_accept(message,address):
    user_id = message.from_user.id
    products = database.get_product_name()
    if message.text == 'Подтвердить':
        database.delete_cart(user_id)
        bot.send_message(user_id,f'Вы подтвердили заказ на {address} адрес',reply_markup=ReplyKeyboardRemove())

    elif message.text == 'Отменить':
        bot.send_message(user_id,'Вы отменили заказ',reply_markup=ReplyKeyboardRemove())

    bot.send_message(user_id,'Меню',reply_markup=buttons.main_menu_kb(products))

@bot.callback_query_handler(lambda call: int(call.data) in database.get_product_id())
def get_user_product(call):
    user_id = call.message.chat.id
    users[user_id]={'pr_name':call.data, 'pr_count': 1}
    message_id = call.message.message_id
    bot.edit_message_text('Выберите количество', chat_id=user_id, message_id=message_id ,reply_markup=buttons.choose_product_count())

bot.polling(non_stop=True)
