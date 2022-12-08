import time
import logging

from aiogram import Bot, Dispatcher, executor, types

import telebot

TOKEN = "5876245431:AAHOV3iwucQIVu-fyGNL7QcjyUcDj4xKmr8"
MASSAGE = "Как твои результаты в программирования {}?"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Обрабатываются все сообщения, содержащие команды '/start'.
@dp.message_handler(commands=['start'])
def handle_start(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    user_full_name = message.from_user.full_name
    logging.info(f'{user_id=} {user_full_name=} {time.asctime()}')

    return message.reply(f'Приветствую, {user_full_name}!')

    for i in range(20):
        time.sleep(60*60*24)

        return bot.send_message(user_id, MASSAGE.format(user_name))



# Обрабатывается все документы и аудиозаписи
@dp.message_handler(content_types=['document', 'audio'])
def handle_docs_audio(message: types.Message):
    pass

@dp.message_handler(content_types=['text', ])
def handle_text(message: types.Message):
    user_name = message.from_user.first_name
    return message.reply(f'Отлично {user_name}!')

@dp.message_handler(content_types=['photo', ])
def handle_photo(message: types.Message):
    user_name = message.from_user.first_name
    return message.reply(f'Интересное изображение {user_name}!')





if __name__ == '__main__':
    executor.start_polling(dp)