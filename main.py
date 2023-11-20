from telebot.async_telebot import AsyncTeleBot, types
import asyncio


"""бот заказан компанией, обслуживающей лифты, логика работы простейшая - бот интегрируется в чаты жильцов 
многоквартирных домов, и как только в чате упоминается слово 'лифт' - пользователю по его id приходит
сообщение о том что слово 'лифт' обнаружено в 'таком-то' чате"""


# Замените 'YOUR_BOT_TOKEN' на токен вашего бота
TOKEN = 'YOUR_BOT_TOKEN'
bot = AsyncTeleBot(TOKEN)


@bot.message_handler(commands=['start'])
async def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn1 = types.KeyboardButton('Запуск бота!')
    markup.add(btn1)
    msg = '<b>ДЛЯ ЗАПУСКА БОТА ЖМИ КНОПКУ</b>' \
          '\n<b>Запуск бота! - внизу экрана</b>' \
          '\nПосле этого отправь боту любое сообщение' \
          '\n\nЕсли бот работает, то при появлении' \
          '\nв группе, которой он управляет, ' \
          '\nсообщений со словом <b>лифт</b>,' \
          '\nтебе будут приходить сообщения от него'
    await bot.send_message(message.chat.id, msg, parse_mode='html', reply_markup=markup)


@bot.message_handler()
async def handle_messages(message):
    # Проверяем, является ли сообщение из группового чата и содержит ли ключевое слово "лифт"
    # if message.chat.type == 'group' and 'лифт' in message.text.lower():
    if 'лифт' in message.text.lower():
        # Отправляем уведомление другому контакту
        await send_notification(message)


@bot.message_handler()
async def send_notification(message):
    try:
        # Получаем информацию о чате
        chat_info = await bot.get_chat(message.chat.id)
        chat_title = chat_info.title
        # Получаем ссылку на чат
        chat_link = chat_info.invite_link

        # Формируем сообщение с информацией о чате
        notification_text = f"Обнаружено ключевое слово 'лифт' в чате '{chat_title}' !" \
                            f"\n\nСсылка на чат:\n{chat_link}"

        # Замените 'TARGET_USER_ID' на ID пользователя (просто число, без кавычек!),
        # которому будет отправлено уведомление
        target_user_id = 'TARGET_USER_ID'

        # Отправляем уведомление целевому пользователю
        await bot.send_message(target_user_id, notification_text)
    except Exception as e:
        print(f"Ошибка при отправке уведомления: {e}")


# запускаем бот в асинхронном режиме >
async def run():
    await bot.polling(none_stop=True)

asyncio.run(run())


