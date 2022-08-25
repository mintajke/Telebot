import telebot
import config


class Mem:
    def __init__(self, name, img_name, description, origin, meaning, url):
        self.name = name
        self.img_name = img_name
        self.description = description
        self.origin = origin
        self.meaning = meaning
        self.url = url

    def send_mem(self, message, bot):

        bot.send_message(message.chat.id, '<b>' + self.name + '</b>', parse_mode='html')
        if self.img_name:
            with open(f"images/{self.img_name}", "rb") as photo:
                bot.send_photo(message.chat.id, photo)
            bot.send_message(message.chat.id, self.description)

        i = 0
        bot.send_message(message.chat.id, '\n<b>Происхождение</b>\n', parse_mode='html')
        while i < config.ORIGIN_LINES and i < len(self.origin):
            bot.send_message(message.chat.id, self.origin[i])
            i += 1

        if len(self.meaning):
            i = 0
            bot.send_message(message.chat.id, '\n<b>Значение</b>\n', parse_mode='html')
            while i < config.MEANING_LINES and i < len(self.meaning):
                bot.send_message(message.chat.id, self.meaning[i])
                i += 1
            # bot.send_message(message.chat.id, self.url)
