import telebot, time

bot = telebot.TeleBot("6323022590:AAH7citiSq3jXgPXuaky2zAUd7XJfFcx2r4")
st_name = "Чипчилинка"
st_energy = 70
st_satiety = 10
st_happiness = 100
all_pets = {'userid': {'n': 'Чипчилинка', 'e': 70, 's': 10, 'h': 100}}


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,
                     '👋 Привет!👋\nЭто тамагочи-бот!\nПиши /pet, чтобы завести питомца (или узнать о его '
                     'состоянии, если он у тебя уже есть)! 😸')
    while True:
        time.sleep(3600)
        if message.from_user.id in all_pets:
            all_pets[message.from_user.id]['h'] -= 5
            all_pets[message.from_user.id]['s'] -= 1
            all_pets[message.from_user.id]['e'] -= 3
            react_is_ok(message.from_user.id)

def get_stats(pet_id):
    return f'\nЕго состояние:\n⚡ Энергия - {all_pets[pet_id]["e"]}\n😋 Сытость - {all_pets[pet_id]["s"]}\n☺️ Счастье - {all_pets[pet_id]["h"]}'


@bot.message_handler(commands=['pet'])
def pet(message):
    if message.from_user.id in all_pets:
        header = f'😺 Твой питомец {all_pets[message.from_user.id]["n"]} 😺'
        bot.send_message(message.chat.id,
                         f'{header}\n{"-" * len(header) * 2}\n{get_stats(message.from_user.id)}')
    else:
        bot.send_message(message.chat.id, 'Ты завёл себе питомца! 😍\nСейчас его зовут "Чипчилинка", но ты можешь '
                                          'поменять '
                                          'имя командой /name!')
        all_pets[message.from_user.id] = {'n': 'Чипчилинка', 'e': 70, 's': 10, 'h': 100}


@bot.message_handler(commands=['name'])
def new_name(message):
    if message.text != '/name':
        if message.from_user.id in all_pets:
            all_pets[message.from_user.id]['n'] = message.text.lstrip('/name ')
            bot.send_message(message.chat.id, f'💬 Имя питомца изменено на {message.text.lstrip("/name ")}')
        else:
            bot.send_message(message.chat.id, 'Ой... Похоже, у тебя ещё нет питомца! ❌\nЗаведи его командой /pet!')
    else:
        bot.send_message(message.chat.id, f'❌ Используйте /name <имя питомца>!')


def check(pet_id):
    if all_pets[pet_id]['e'] <= 0:
        return 'no_energy'
    elif all_pets[pet_id]['s'] <= 0:
        return 'no_food'
    elif all_pets[pet_id]['h'] <= 0:
        return 'unhappy'
    else:
        return 'ok'


def react_is_ok(pet_id):
    state = check(pet_id)
    if state == 'no_energy':
        bot.send_message(pet_id, 'Твой питомец умер от истощения( 😭\nНадо было кормить его и следить за режимом сна!')
        del all_pets[pet_id]
    if state == 'no_food':
        bot.send_message(pet_id, 'Твой питомец умер от голода( 😭\nНадо было кормить его чаще!')
        del all_pets[pet_id]
    if state == 'unhappy':
        bot.send_message(pet_id, 'Твой питомец умер от тоски( 😭\nНадо было чаще играть с ним!')
        del all_pets[pet_id]


def feed(u):
    global all_pets
    all_pets[u]['s'] += 10
    all_pets[u]['e'] += 5


def play(u):
    global all_pets
    all_pets[u]['s'] -= 10
    all_pets[u]['e'] -= 5
    all_pets[u]['h'] += 10


def sleep(u):
    global all_pets
    all_pets[u]['s'] -= 5
    all_pets[u]['h'] -= 5
    all_pets[u]['e'] = 70


@bot.message_handler(commands=['feed'])
def f(message):
    if message.from_user.id in all_pets:
        feed(message.from_user.id)
        bot.send_message(message.chat.id, f'Твой питомец {all_pets[message.from_user.id]["n"]} покушал! 😋\n{get_stats(message.from_user.id)}')
        react_is_ok(message.from_user.id)
    else:
        bot.send_message(message.chat.id, 'Ой... Похоже, у тебя ещё нет питомца! ❌\nЗаведи его командой /pet!')


@bot.message_handler(commands=['play'])
def p(message):
    if message.from_user.id in all_pets:
        play(message.from_user.id)
        bot.send_message(message.chat.id, f'Ты поиграл с {all_pets[message.from_user.id]["n"]}! 🐶\n{get_stats(message.from_user.id)}')
        react_is_ok(message.from_user.id)
    else:
        bot.send_message(message.chat.id, 'Ой... Похоже, у тебя ещё нет питомца! ❌\nЗаведи его командой /pet!')


@bot.message_handler(commands=['sleep'])
def s(message):
    if message.from_user.id in all_pets:
        sleep(message.from_user.id)
        bot.send_message(message.chat.id, f'Твой питомец {all_pets[message.from_user.id]["n"]} поспал 😴\n{get_stats(message.from_user.id)}')
        react_is_ok(message.from_user.id)
    else:
        bot.send_message(message.chat.id, 'Ой... Похоже, у тебя ещё нет питомца! ❌\nЗаведи его командой /pet!')


@bot.message_handler(commands=['mood'])
def mood(message):
    if message.from_user.id in all_pets:
        pet_data = all_pets[message.from_user.id]
        if pet_data['h'] <= 20:
            bot.send_sticker(message.chat.id, sticker='CAACAgUAAxkBAALE4WTc1seGymXfN45'
                                                      '-ftBbAAEkKI0JRAAClQUAAlU7wFf_jvDGDvn3-zAE')
            bot.send_message(message.chat.id, 'Твой питомец грустит 😓\nПоиграй с ним!')
        elif pet_data['s'] <= 5:
            bot.send_sticker(message.chat.id, sticker='CAACAgUAAxkBAALE5GTc1sc6FU3akviIoGTeHwkNDib1AAJjAwACMCHAV1fJqKKDJ4OuMAQ')
            bot.send_message(message.chat.id, 'Твой питомец голоден! 😖\nПокорми его!')
        elif pet_data['s'] >= 40:
            bot.send_sticker(message.chat.id, sticker='CAACAgUAAxkBAALE4mTc1sd076_VFtKtOzhvT6qFSJKWAAKFBQAC'
                                                      '-KnAV4W86xrLqts4MAQ')
            bot.send_message(message.chat.id, 'О нет! Твой питомец слишком много съел! 🥴\nПоиграй с ним скорее!')
        elif pet_data['e'] <= 10:
            bot.send_sticker(message.chat.id, sticker='CAACAgUAAxkBAALE42Tc1sf7SU9hEhcn1J810-UiIjRCAAKGBQAC0OzBV'
                                                      '-UezgkhsFdfMAQ')
            bot.send_message(message.chat.id, 'Твой питомец очень устал и хочет спать! 🥱')
        else:
            bot.send_sticker(message.chat.id, sticker='CAACAgUAAxkBAALE4GTc1sehLcWE7zMIsGlzixIBn2mCAAINBQACejDBV4i'
                                                      '-Pejl_tN1MAQ')
            bot.send_message(message.chat.id, 'Твой питомец полон сил и готов играть с тобой!')
    else:
        bot.send_message(message.chat.id, 'Ой... Похоже, у тебя ещё нет питомца! ❌\nЗаведи его командой /pet!')


bot.polling(none_stop=True)
