import telebot
from telebot import types
import random
import wikipedia
import re
import urllib.request
import info


bot = telebot.TeleBot(token=info.token)
chat_id = info.chat_id
wikipedia.set_lang("ru")


# Функция, обрабатывающая команду /start
@bot.message_handler(commands=['start'])
def start_message(message):
    sti = open('avatar.png', 'rb')
    bot.send_sticker(message.chat.id, sti)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Как меня зовут')
    btn2 = types.KeyboardButton('Мои навыки')
    btn3 = types.KeyboardButton('Пандора')
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id,
                     "Привет {0.first_name} это Телеграм_бот ✌️".format(message.from_user, bot.get_me()),
                     reply_markup=markup)


# Функция, обрабатывающая команду /help
@bot.message_handler(commands=['help'])
def help_command(message):
    bot.send_message(
        message.chat.id,
        '1) /hobby Навыки персонажа: 🏓\n' +
        '2) /help Если вы что-то забыли: 📒\n')


# Функция, обрабатывающая команду /hobby
@bot.message_handler(commands=['hobby'])
def show_hobbies(message):
    bot.send_message(message.chat.id, my_name() + hobby(), parse_mode='HTML')


@bot.message_handler(content_types=['photo'])
def photo(message):
    # Получим ID фото
    file_id = message.photo[-1].file_id
    # Получаем путь, где лежит фото на сервере Телеграмма
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open("image.jpg", 'wb') as new_file:
        new_file.write(downloaded_file)


@bot.message_handler(content_types=['audio'])
def handle_docs_audio(message):
    # Получим ID аудио
    audio_id = message.audio.file_id
    # Получаем путь, где лежит аудио файл на сервере Телеграмма
    file_info = bot.get_file(audio_id)
    # Формируем ссылку и скачиваем файл
    urllib.request.urlretrieve(f'http://api.telegram.org/file/bot{info.token}/{file_info.file_path}',
                               file_info.file_path)


@bot.message_handler(content_types=['document'])
def handle_docs_audio(message):
    document_id = message.document.file_id
    file_info = bot.get_file(document_id)
    urllib.request.urlretrieve(f'http://api.telegram.org/file/bot{info.token}/{file_info.file_path}',
                               file_info.file_path)


@bot.message_handler(content_types=['sticker'])
def handle_docs_audio(message):
    sticker_id = message.sticker.file_id
    file_info = bot.get_file(sticker_id)
    urllib.request.urlretrieve(f'https://api.telegram.org/file/bot{info.token}/{file_info.file_path}',
                               file_info.file_path)


def getwiki(s):
    try:
        ny = wikipedia.page(s)
        # Получаем первые 800 символов
        wikitext = ny.content[:800]
        # Разделяем по точкам
        wikimas = wikitext.split('.')
        # Отбрасываем всЕ после последней точки
        wikimas = wikimas[:-1]
        # Создаем пустую переменную для текста
        wikitext2 = ''
        # Проходимся по строкам, где нет знаков == (то есть все, кроме заголовков)
        for x in wikimas:
            if not ('==' in x):
                # Если в строке осталось больше трех символов, добавляем ее к нашей переменной
                # и возвращаем утерянные при разделении строк точки на место
                if len((x.strip())) > 3:
                    wikitext2 = wikitext2 + x + '.'
            else:
                break
        # При помощи регулярных выражений убираем разметку
        wikitext2 = re.sub('\([^()]*\)', '', wikitext2)
        wikitext2 = re.sub('\([^()]*\)', '', wikitext2)
        wikitext2 = re.sub('\{[^\{\}]*\}', '', wikitext2)

        return wikitext2

    except Exception as e:
        return 'Извините, я не понял ваш вопрос'


def my_name():
    str_format = (f'<b>👋 Как меня зовут</b>\n\n' +
                  f'<b>Имя: </b> <i>{info.character["name"]}</i>\n' +
                  f'<b>Возраст: </b><i>{info.character["age"]}</i>\n' +
                  f'<b>Планета: </b><i>{info.character["adress"]}</i>\n\n')
    return str_format


def hobby():
    str_format = (f'<b>🏓 Мои навыки</b>\n\n' +
                  f'<b>Навыки: </b><i> {info.character["hobby"][0]} и {info.character["hobby"][1]}</i>\n\n')
    return str_format


@bot.message_handler(content_types=['text'])
def func(message):
    if message.chat.type == 'private':
        if message.text == 'Как меня зовут':
            bot.send_message(message.chat.id, my_name(), parse_mode='HTML')

        elif message.text == 'Мои навыки':
            bot.send_message(message.chat.id, hobby(), parse_mode='HTML')

        elif message.text == 'Пандора':
            bot.send_message(message.chat.id, getwiki('Планета Пандора'))

        else:
            question = message.text.strip().lower()
            if question in info.telebot_responses:
                response = random.choice(info.telebot_responses[question])
                bot.send_message(message.chat.id, text=response)
            else:
                bot.send_message(message.chat.id, text='Извините, я не понял ваш вопрос')


bot.polling(none_stop=True)
