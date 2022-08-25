import telebot
import parsing
import random
import config
import mem_class

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    mess = f'Привет, <b>{message.from_user.first_name}</b> \nЭтот бот будет показывать мемы по запросу.\n/help чтобы узнать доступные команды.'
    bot.send_message(message.chat.id, mess, parse_mode='html')


@bot.message_handler(commands=['help'])
def help(message):

    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    start = telebot.types.KeyboardButton('/start')
    help = telebot.types.KeyboardButton('/help')
    rand = telebot.types.KeyboardButton('/rand')

    markup.add(start, help, rand)

    mess = 'Доступные команды:\n/rand - случайный мем\n/rand 2007 - случайный мем 2007 года (2007-2022)'
    bot.send_message(message.chat.id, mess, reply_markup=markup)


#@bot.message_handler(content_types=['photo'])
#def get_user_photo(message):
#    bot.send_message(message.chat.id, 'Nice one')


@bot.message_handler(commands=['website'])
def website(message):
   markup = telebot.types.InlineKeyboardMarkup()
   markup.add(telebot.types.InlineKeyboardButton("memopedia.ru", url="https://memepedia.ru"))
   bot.send_message(message.chat.id, 'Мемы честно взяты отсюда:', reply_markup=markup)


@bot.message_handler(commands=['rand'])
def rand(message):
    "Тут будет выдача рандомного мема"
    message_words = message.text.split()
    if len(message_words) > 1:
        year = int(message_words[-1])
    else:
        year = random.randint(2007, 2022)

    bot.send_message(message.chat.id, f"Возвращаемся в {year} год...")

    name, img_name, description, origin, meaning, url = random_from_year(year)
    cur_mem = mem_class.Mem(name, img_name, description, origin, meaning, url)
    cur_mem.send_mem(message, bot)


# def random_from_all():
#     "Определяем рандомно год, дальше как в random_year"
#
#     rnd_int = random.randint(2007, 2022)
#     return random_from_year(rnd_int)


def random_from_year(year):
    "Тут бyдeт выдача рандомного мема заданного года"

    with open(f"mem_urls/mems_info") as f:
        for line in f:
            cur_line = line.split()
            if int(cur_line[0]) == year:
                num_mem = int(cur_line[1])
                break
    rnd_int = random.randint(0, num_mem-1)
    with open(f"mem_urls/{year}") as f:
        for index, line in enumerate(f):
            if index == rnd_int:
                cur_line = line.split()
                break

    return parsing.parse(cur_line[-1])
    #return parsing.parse('https://memepedia.ru/slishkom-navyazchivaya-devushka-overly-attached-girlfriend/')


@bot.message_handler(content_types=['text'])
def get_user_text(message):
    if message.text == "Привет":
        bot.send_message(message.chat.id, "И тебе привет", parse_mode='html')
    else:
        bot.send_message(message.chat.id, "WAT?", parse_mode='html')


def main():
    bot.polling(none_stop=True)


if __name__ == '__main__':
    main()
