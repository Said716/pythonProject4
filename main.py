import sqlite3
import telebot
import db
from telebot import types
from SimpleQIWI import *
from time import sleep
from telebot.types import LabeledPrice


pay = []
tmp = db.bd('bot_db.db')

buyy = '381764678:TEST:43830'
bot = telebot.TeleBot('5637407120:AAE9rlKzhvMpUQ1XqKztZHJVwiM6nX9pjCU')
@bot.message_handler(commands = ['start'])

def start(m):
    bot.send_message(m.chat.id , 'Добро пожаловать, напишите название товара, чтобы получить информацию о нем ')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("посмотреть наличие ")

    item2 = types.KeyboardButton("купить")
    markup.add(item1)
    markup.add(item2)
    bot.send_message(m.chat.id,'нажмите на кнопку чтобы узнать информацию',reply_markup=markup)


@bot.message_handler()
def answer(m):
    if m.text == 'посмотреть наличие' :
        mesg = bot.send_message(m.chat.id,'Введите товар')
        bot.register_next_step_handler(mesg,quantity)
    if m.text == 'купить':
        mesg = bot.send_message(m.chat.id, 'Введите товар')
        bot.register_next_step_handler(mesg, buy)
def buy(m):

    z = tmp.sms(m.text.capitalize())
    print(z)

    x = []
    for j in z :
        x.append(j[3])
    if len(x) == 1 :
        prices = [LabeledPrice(label='Working Time Machine', amount=80000)]

        bot.send_invoice(chat_id=m.chat.id, title=m.text, description='описание',
                         invoice_payload='some-invoice-payload-for-internal-use',
                         provider_token=buyy, currency='RUB',
                         prices=prices , start_parameter="test-start-parameter")
        pay.append(m.text)
    else:

        for l in x:
            bot.send_message(m.chat.id,l)
        d = bot.send_message(m.chat.id,'Введите фабрику которую вы хотите')

        bot.register_next_step_handler(d, kkk, m.text)


def kkk(m,f):
    r = tmp.price(m.text,f)
    r = r[0]
    r = r[0] + '00'

    prices = [LabeledPrice(label='Working Time Machine', amount=r)]

    bot.send_invoice(chat_id=m.chat.id, title=f ,description=m.text,
                    invoice_payload='some-invoice-payload-for-internal-use',
                    provider_token=buyy, currency='RUB',
                    prices=prices , start_parameter="test-start-parameter")
    pay.append([f,m.text])







def quantity(m):
    v = tmp.sms(m.text.capitalize())
    if v == []:
        bot.send_message(m.chat.id, 'такого товара нет')
    else:
        for i in v:
            if int(i[2]) < 10:
                g = i[0] + '\n'+ '< 10'
            elif int(i[2]) > 50:
                g = i[0] + '\n' + '> 50'
            else:
                g = i[0] + '\n' + i[2]



            bot.send_message(m.chat.id, g)
@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True,
                                  error_message="Aliens tried to steal your card's CVV, but we successfully protected your credentials,"
                                                " try to pay again in a few minutes, we need a small rest.")


@bot.message_handler(content_types=['successful_payment'])
def got_payment(message):

    bot.send_message(message.chat.id,
                     'Hoooooray! Thanks for payment! We will proceed your order for `{} {}` as fast as possible! '
                     'Stay in touch.\n\nUse /buy again to get a Time Machine for your friend!'.format(
                         message.successful_payment.total_amount / 100, message.successful_payment.currency),
                     parse_mode='Markdown')
    r = pay[-1]
    tmp.update(r[0],r[1])
def qiwi(m,api ):
    token = '15f88e9a2a799551757fb4a3875e4706'
    phone = '+79214647777'
    api = QApi(token=token, phone=phone)
    price = 10
    comment = api.bill(price)
    api.start()

    if m == 'купить ':
        bot.send_message(m.chat.id,comment)
        while True:
            if api.check(comment):
                bot.send_message(m.chat.id,'платеж прошел ')
            else:
                bot.send_message(m.chat.id,'оплата не проходила')
                break
            sleep(1)
        api.stop()





bot.infinity_polling()
#
# df = pandas.read_excel('table_to_test2.xlsx')
#
#
# df = df.drop(0, axis=0)
# df.rename(columns={'Unnamed: 0': 'Name', 'Unnamed: 1':'Price', 'Unnamed: 2': 'Quantity', 'Unnamed: 3':'Diller'},inplace = True )
# print(df)
#
# connect = sqlite3.connect('bot_db.db')







# cursor = connect.cursor()
#
# create_table = '''CREATE TABLE IF NOT EXISTS bot_table(
#                    Name text NOT NULL,
#                    Price text NOT NULL,
#                    Quantity text NOT NULL,
#                    Diller text NOT NULL); '''
#
# cursor.execute(create_table)
# df.to_sql('bot_table', con=connect, if_exists='append', index=False)


