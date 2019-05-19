import telebot
import Database
import dateparser
import matplotlib.pyplot as plt

TOKEN = '528060291:AAHLkR2sAMoF_18scEiRCGBKWKU2clh0lA8'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    sent = bot.send_message(message.chat.id, 'Что ты хочешь узнать сегодня?')
    bot.register_next_step_handler(sent, hello)


def hello(message):
    if message.text == 'help':
        bot.send_message(message.chat.id, '1)Введите TOP-DOC <число>, чтобы узнать последний 10 новостей\n'
                                          '2)Введите TOP-TITLE-10, чтобы узнать последние 10 тем новостей\n'
                                          '3)Введите Describe_topic <Name> (вводить само название, через пробел), чтобы вывести статистику по теме:\n'
                                          '     а) количество документов в заголовке\n'
                                          '     б) средняя длина документа (в словах)\n'
                                          '     в) 40 случайных слов из текстов с указанием их частот, представленных'
                                          'в виде диаграммы\n'
                                          '4)Закончить работу Bye')
    if 'Describe_topic' in message.text:
        k = str(message.text)
        simb = k.find(' ')
        name = message.text[simb + 1: ]
        try:
            p = Database.describe_topic(name)
            b = open('my.png', 'rb')
            bot.send_photo(message.chat.id, b)
            bot.send_message(message.chat.id, 'Средняя длина документов {} (в словах)'.format(p[0]))
            bot.send_message(message.chat.id, 'Количество документов {} (в заголовке)'.format(p[1]))
        except:
            bot.send_message(message.chat.id, 'Боюсь, этой новости у меня не нашлось.(')
        bot.register_next_step_handler(bot.send_message(message.chat.id, 'Что-то еще?'), hello)
    elif message.text == 'Bye':
        bot.send_message(message.chat.id, 'До скорой встречи!')
    elif 'TOP-DOC' in message.text:
        number = message.text.split()[1]
        n = Database.top_n(number)
        for i in n:
            bot.send_message(message.chat.id, 'Это: {}'.format(str(i[0])))
        bot.register_next_step_handler(bot.send_message(message.chat.id, 'Что-то еще?'), hello)
    elif 'TOP-TITLE' in message.text:
        n = Database.top(10)
        for i in n:
            bot.send_message(message.chat.id, 'Это: {}'.format(str(i[0])))
        bot.register_next_step_handler(bot.send_message(message.chat.id, 'Что-то еще?'), hello)
    else:
        bot.register_next_step_handler(bot.send_message(message.chat.id, 'Что-то еще?'), hello)


bot.polling()
