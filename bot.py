import telebot
from collections import defaultdict

bot = telebot.TeleBot('Token')
START, NumberPhone, NICKNAME, LoadMess = range(4)
USER_STATE = defaultdict(lambda: START)

def get_state(message):
    return USER_STATE[message.chat.id]
def update_state(message, state):
    USER_STATE[message.chat.id] = state

USERS = defaultdict(lambda:{})
def update_DataPeople(user_id, key, value):
    USERS[user_id][key] = value
def get_dataPeople(user_id):
    return USERS[user_id]

@bot.message_handler(commands=['help'])
def start_help(message):
    bot.send_message(message.chat.id, 'Дополнительные вопросы можно задать сюда @Newpeepl')


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, '🎁Книга - подарок, с помощью которой ты начнёшь зарабатывать на Инстаграм:')
    pdf234 = open('/Users/zombie/Desktop/salesBot/salesBook.pdf', 'rb')
    bot.send_document(message.chat.id, pdf234)
    bot.send_message(message.chat.id, 'И это ещё не все 🙌\nТы хочешь зарабатывать с блога в Инстаграм?\n💣Бесплатный вебинар по продвижению Инстаграм!Все самые крутые бесплатные и платные методы, алгоритмы Инстаграм, повышение охватов, увеличение количества подписчиков, продажи через Инстаграм и многое многое другое!\nПосле вебинара ты 💯 сможешь применить всю полученную информацию и начать монетизировать свой аккаунт!\nТы в деле🙌скажи да!')


@bot.message_handler(func=lambda message: get_state(message) == START)
def handle_message(message):
    update_DataPeople(message.chat.id, 'Ваш ответ', message.text)
    bot.send_message(message.chat.id, '🔺Напиши  свой номер телефона🔻')
    update_state(message, NumberPhone)

@bot.message_handler(func=lambda message: get_state(message) == NumberPhone)
def handle_NumberPhone(message):
    update_DataPeople(message.chat.id, 'Телефон', message.text)
    bot.send_message(message.chat.id, '🔺Как вас зовут?🔻')
    update_state(message, NICKNAME)

@bot.message_handler(func=lambda message: get_state(message) == NICKNAME)
def handle_load(message):
    update_DataPeople(message.chat.id, 'Имя', message.text)
    DataPeople = get_dataPeople(message.chat.id)
    bot.send_message(message.chat.id, '🔺Всё верно? Если верно то напиши "да"🔻,\n{}'.format(DataPeople))
    update_state(message, LoadMess)

@bot.message_handler(func=lambda message: get_state(message) == LoadMess)
def handle_confirm(message):
    if 'да' in message.text.lower():
           bot.send_message(message.chat.id, '🔺Заявка принята🔻,\n{}'.format(USERS))
           bot.send_message(169893874, '🔺Новая заявка🔻,\n{}'.format(USERS))
    update_state(message, START)

if __name__ == '__main__':
    bot.polling()
