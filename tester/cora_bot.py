import telebot
from django.http import HttpResponse

bot = telebot.TeleBot('6924477556:AAH3pYP8AzQJXia27bgxAW1srTfAAaCaHC0')


def reqs(request):
    if request.method == "POST":
        update = telebot.types.Update.de_json(request.body.decode('utf-8'))
        bot.process_new_updates([update])

    return HttpResponse('<h1>Ты подключился!</h1>')


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.from_user.id, 'start')