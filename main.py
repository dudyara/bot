import telebot
from telebot import types

bot = telebot.TeleBot('1415577543:AAHDlrHt34mqq6FcnHQcAGh01DteR-2fXjc')

name = ''
surname = ''
age = 0


@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == '/reg':
        bot.send_message(message.from_user.id, "Ты кто?")
        bot.register_next_step_handler(message, get_name)
    elif message.text == "Привет":
        bot.send_message(message.from_user.id, "Пошел нахуй")
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Напиши Привет или /reg")
    else:
        bot.send_message(message.from_user.id, "Напиши /help")


def get_name(message):  # получаем фамилию
    global name
    name = message.text
    bot.send_message(message.from_user.id, 'А я ебу кто такой ' + name + '? Фамилию скажи, еблан.')
    bot.register_next_step_handler(message, get_surname)


def get_surname(message):
    global surname
    surname = message.text
    bot.send_message(message.from_user.id, 'Сколько тебе лет, мудила?')
    bot.register_next_step_handler(message, get_age)
    bot.send_sticker(message.chat.id, 'CAADAgADZgkAAnlc4gmfCor5YbYYRAI')


def get_age(message):
    global age
    while age == 0:  # проверяем что возраст изменился
        try:
            age = int(message.text)  # проверяем, что возраст введен корректно
        except Exception:
            bot.send_message(message.from_user.id, 'Цифрами, еблан')
    keyboard = types.InlineKeyboardMarkup() # наша клавиатура
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')  # кнопка «Да»
    keyboard.add(key_yes)  # добавляем кнопку в клавиатуру
    key_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
    keyboard.add(key_no)
    question = 'Тебе ' + str(age) + ' лет, тебя зовут ' + name + ' ' + surname + '?'
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes":
        bot.send_message(call.message.chat.id, 'Данные сохранены, все, уебывай.')
    elif call.data == "no":
        bot.send_message(call.message.chat.id, 'А нахуй ты мне неправильные данные говоришь?')


bot.polling(none_stop=True, interval=0)
