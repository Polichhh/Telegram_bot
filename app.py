import telebot
from config import keys, TOKEN
from extensions import ConvExcep, CripConverter
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message: telebot.types.Message):
    text = 'Чтобы начать работу, введите боту команду в формате: две валюты и цифру (все через пробел)\n \nимя валюты \n\
в какую валюту перевести \n\
количество переводимой валюты \n\nУвидеть список доступных валют: /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def val(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise ConvExcep('Не понимаю. Напишите две валюты и цифру.')
        base, quote, amount = values
        total = CripConverter.convert(base, quote, amount)
    except ConvExcep as e:
        bot.reply_to(message, f'{e}')
    except Exception as e:
        bot.reply_to(message, f'{e}')
    else:
        text = f'Цена {amount} {base} в {quote} - {total}'
        bot.send_message(message.chat.id, text)

bot.polling(none_stop=True)