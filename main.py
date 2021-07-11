import telebot
from telebot import types
from SimpleQIWI import *
import random

with open("config.txt", "r") as f:
    qiwi_number = f.readline().split(": ")[1].replace("\n", "")
    qiwi_token = f.readline().split(": ")[1].replace("\n", "")
    tg_token = f.readline().split(": ")[1].replace("\n", "")

api = QApi(token=qiwi_token, phone=qiwi_number)

bot = telebot.TeleBot(tg_token, parse_mode=None)

buffer = []

markup = types.ReplyKeyboardMarkup(row_width=2)
itembtn1 = types.KeyboardButton('Примеры фоток')
itembtn2 = types.KeyboardButton('Каталог')
itembtn3 = types.KeyboardButton('FAQ')
markup.add(itembtn1, itembtn2, itembtn3)

markup1 = types.ReplyKeyboardMarkup(row_width=2)
itembtn4 = types.KeyboardButton('14-17 лет фото/видео рандомный архив')
itembtn5 = types.KeyboardButton('10-13 лет фото/видео рандомный архив')
itembtn6 = types.KeyboardButton('1 месяц подписки')
itembtn7 = types.KeyboardButton('3 месяца подписки')
itembtn8 = types.KeyboardButton('Подписка навсегда')
itembtn9 = types.KeyboardButton('Назад')
markup1.add(itembtn4, itembtn5, itembtn6, itembtn7, itembtn8, itembtn9)

markup2 = types.ReplyKeyboardMarkup(row_width=2)
itembtn10 = types.KeyboardButton('Проверить оплату')
markup2.add(itembtn10, itembtn9)


def generate_link(amount, comment, number=qiwi_number):
    link = "https://qiwi.com/payment/form/99?extra[%27accountType%27]=number&extra[%27account%27]=" + str(number) + \
           "&extra[%27comment%27]=" + str(comment) + "&currency=643&amountInteger=" + str(amount) + "&amountFraction=0 "
    return link


def check(com):
    history = api._get_payments(rows=20)
    history = str(history).split("}, {'txnId':")
    for i in history:
        a = i.find("comment") + 11
        b = i.find("currencyRate")
        c = i.find("'amount': ")
        d = i.find("'currency'")
        comment = i[a:b].replace("', '", "")
        summ = int(float(i[c:d].replace("'amount': ", "").replace(", ", "")))
        if com == comment:
            return True, summ
        return False, 0


@bot.message_handler()
def message_check(message):
    print(message)
    if message.text == "/start" or message.text == "Назад":
        bot.send_message(message.chat.id, "Привет. Здесь ты можешь покупать и получать ссылки на отдельные паки фоток "
                                          "и видео, так и купить подписку на закрытый канал, где каждый день будут "
                                          "публиковатся лучшие из них. Оплата доступна через QIWI.",
                         reply_markup=markup)
    if message.text == "Примеры фоток":
        try:
            photo = open('preview.png', 'rb')
            bot.send_photo(message.chat.id, photo)
        except:
            pass
    if message.text == "FAQ":
        bot.send_message(message.chat.id, "Какими способами доступна оплата? Только QIWI.\nЧто я получу после покупки "
                                          "пака? Ссылку на архив загруженный на Яндекс.Диск\nЧто я получу после "
                                          "покупки подписки? Инвайт в закрытый канал, где каждый день будут "
                                          "публиковатся лучшие паки")
    if message.text == "Каталог":
        bot.send_message(message.chat.id, "Паки:\n14-17 лет фото/видео рандомный архив - 35р\n10-13 лет фото/видео "
                                          "рандомный архив - 50р\n\nПодписки:\n1 месяц - 75р\n3 месяца - 120р\nНавсегда"
                                          " - 200р\n\nВыберите: ", reply_markup=markup1)
    if message.text == '14-17 лет фото/видео рандомный архив':
        comment = str(random.randint(10000, 20000))
        bot.send_message(message.chat.id, "Ссылка для оплаты: " + str(generate_link(35, comment)), reply_markup=markup2)
        buffer.append(str(message.chat.id)+"/"+str(comment))
    if message.text == '10-13 лет фото/видео рандомный архив':
        comment = str(random.randint(10000, 20000))
        bot.send_message(message.chat.id, "Ссылка для оплаты: " + str(generate_link(50, comment)), reply_markup=markup2)
        buffer.append(str(message.chat.id)+"/"+str(comment))
    if message.text == '1 месяц подписки':
        comment = str(random.randint(10000, 20000))
        bot.send_message(message.chat.id, "Ссылка для оплаты: " + str(generate_link(75, comment)), reply_markup=markup2)
        buffer.append(str(message.chat.id)+"/"+str(comment))
    if message.text == '3 месяца подписки':
        comment = str(random.randint(10000, 20000))
        bot.send_message(message.chat.id, "Ссылка для оплаты: " + str(generate_link(120, comment)), reply_markup=markup2)
        buffer.append(str(message.chat.id)+"/"+str(comment))
    if message.text == 'Подписка навсегда':
        comment = str(random.randint(10000, 20000))
        bot.send_message(message.chat.id, "Ссылка для оплаты: " + str(generate_link(200, comment)), reply_markup=markup2)
        buffer.append(str(message.chat.id)+"/"+str(comment))
    if message.text == 'Проверить оплату':
        for i in buffer:
            if i.split("/")[0] == str(message.chat.id):
                ch = check(str(i.split("/")[1]))
                #ch = check(str(13639))
                if ch[0]:
                    print("+" + str(ch[1]) + "р от ", message)
                    try:
                        photo = open('dick.png', 'rb')
                        bot.send_photo(message.chat.id, photo)
                    except:
                        pass
                else:
                    bot.send_message(message.chat.id, "Деньги еще не пришли")


bot.polling()