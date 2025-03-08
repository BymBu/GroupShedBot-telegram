import telebot
import atexit
import json
import os
import time
import datetime
from datetime import timedelta
import random
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from telebot import types
import pytz



token='YOUR TOKEN'
my_timezone = pytz.timezone('Asia/Irkutsk')


bot = telebot.TeleBot(token)

# Переменные с айди администраторов и чата
ADM = yourIDadm # для /s
chat_id = yourchat_id # для /s
CONSOLE = -1002098012390



def load_calendar():
    try:
        with open('calendar.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}

# Функция для сохранения расписания в файл
def save_calendar(calendar):
    with open('calendar.json', 'w', encoding='utf-8') as f:
        json.dump(calendar, f, ensure_ascii=False, indent=4)

# Загрузка расписания при старте
calendar = load_calendar()
print(calendar)

# Информация о запуске и выключении бота
def on_start():
  print("Бот успешно запущен. 🙄")
  response = f"📌| Бот запущен"
  bot.send_message(CONSOLE, response)

on_start()


def on_stop():
  print("Бот успешно выключен")
  response = f"📌| Бот выключен"
  bot.send_message(CONSOLE, response)


@atexit.register
def exit_handler():
  on_stop()


bot.skip_pending = True


# Месяца для расписания
months_of_year = {
    "01": "Января",
    "02": "Февраля",
    "03": "Марта",
    "04": "Апреля",
    "05": "Мая",
    "06": "Июня",
    "07": "Июля",
    "08": "Августа",
    "09": "Сентября",
    "10": "Октября",
    "11": "Ноября",
    "12": "Декабря"
}



days_of_week = {
    "monday": "Понедельник",
    "tuesday": "Вторник",
    "wednesday": "Среда",
    "thursday": "Четверг",
    "friday": "Пятница",
    "saturday": "Суббота",
    "sunday": "Воскресенье"
}

# Словарь для сопоставления сокращений с полными названиями
days_mapping = {
    "пн": "monday",
    "вт": "tuesday",
    "ср": "wednesday",
    "чт": "thursday",
    "пт": "friday",
    "сб": "saturday",
    "вс": "sunday"
}



# Блок перезарядки
def check_cooldown(bot, message, game, cooldown_time=300):
    """
    Проверяет кулдаун для команды и обновляет время последнего использования.

    :param bot: объект бота (например, telebot.TeleBot)
    :param message: сообщение, полученное от пользователя
    :param game: название команды (например, 'calendar')
    :param cooldown_time: время кулдауна в секундах (по умолчанию 300 секунд = 5 минут)
    :return: True, если кулдаун прошел, иначе False
    """
    # Путь к файлу с кулдаунами
    cooldown_file = 'cooldown.json'

    # Чтение данных из JSON файла
    try:
        with open(cooldown_file, 'r') as file:
            timers = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        timers = {}

    # Текущее время
    current_time = datetime.datetime.now()

    chat_id = str(message.chat.id)

    # Проверка, есть ли запись для данной команды
    if game in timers:
        chat_id = str(message.chat.id)

        # Проверяем, был ли выполнен запрос для этого чата
        if chat_id in timers[game]:
            last_time = datetime.datetime.strptime(timers[game][chat_id], "%Y-%m-%d %H:%M:%S")
            time_difference = current_time - last_time

            # Если время до кулдауна меньше, чем заданный предел
            if time_difference.total_seconds() < cooldown_time:
                remaining_time_seconds = cooldown_time - time_difference.total_seconds()

                # Создаем объект timedelta для оставшегося времени
                remaining_time = timedelta(seconds=remaining_time_seconds)

                # Форматируем оставшееся время в удобочитаемый вид
                remaining_time_str = str(remaining_time).split(".")[0]  # Это уберет микросекунды

                bot.reply_to(message, text=f'❌| Перезарядка! Осталось времени: {remaining_time_str}')
                return False  # Кулдаун активен

    # Если кулдаун прошел или команды еще нет в списке - обновляем время
    if game not in timers:
        timers[game] = {}

    timers[game][chat_id] = current_time.strftime("%Y-%m-%d %H:%M:%S")

    # Сохраняем данные обратно в файл
    with open(cooldown_file, 'w') as file:
        json.dump(timers, file, indent=4)

    return True  # Кулдаун не активен


def check_cooldown_call(bot, message, game, cooldown_time=15):
    """
    Проверяет кулдаун для команды и обновляет время последнего использования.

    :param bot: объект бота (например, telebot.TeleBot)
    :param message: сообщение, полученное от пользователя
    :param game: название команды (например, 'calendar')
    :param cooldown_time: время кулдауна в секундах (по умолчанию 300 секунд = 5 минут)
    :return: True, если кулдаун прошел, иначе False
    """
    # Путь к файлу с кулдаунами
    cooldown_file = 'cooldown.json'

    # Чтение данных из JSON файла
    try:
        with open(cooldown_file, 'r') as file:
            timers = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        timers = {}

    # Текущее время
    current_time = datetime.datetime.now()

    chat_id = str(message.chat.id)

    # Проверка, есть ли запись для данной команды
    if game in timers:
        chat_id = str(message.chat.id)

        # Проверяем, был ли выполнен запрос для этого чата
        if chat_id in timers[game]:
            last_time = datetime.datetime.strptime(timers[game][chat_id], "%Y-%m-%d %H:%M:%S")
            time_difference = current_time - last_time

            # Если время до кулдауна меньше, чем заданный предел
            if time_difference.total_seconds() < cooldown_time:
                remaining_time_seconds = cooldown_time - time_difference.total_seconds()

                # Создаем объект timedelta для оставшегося времени
                remaining_time = timedelta(seconds=remaining_time_seconds)

                # Форматируем оставшееся время в удобочитаемый вид
                remaining_time_str = str(remaining_time).split(".")[0]  # Это уберет микросекунды

                return False  # Кулдаун активен

    # Если кулдаун прошел или команды еще нет в списке - обновляем время
    if game not in timers:
        timers[game] = {}

    timers[game][chat_id] = current_time.strftime("%Y-%m-%d %H:%M:%S")

    # Сохраняем данные обратно в файл
    with open(cooldown_file, 'w') as file:
        json.dump(timers, file, indent=4)

    return True  # Кулдаун не активен


# Блок отправки информации в консоль

def send_console(message):
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    chat_id = message.chat.id
    chat_type = message.chat.type
    chat_name = message.chat.title
    location = message.location
    command = message.text.split()[0]
    response = f"‼️Пользователь @{username} использовал команду {command}!"
    response += f"\n👩🏻‍🦱| ID пользователя: {user_id}"
    response += f"\n👕| Имя пользователя: @{username}"
    response += f"\n📛| Имя: {first_name}"
    response += f"\n📛| Фамилия: {last_name}"
    response += f"\n💻| ID чата: {chat_id}"
    response += f"\n📦| Тип чата: {chat_type}"
    response += f"\n✅| Название чата: {chat_name}"
    response += f"\n🗺️| Локация: {location}"

    bot.send_message(CONSOLE, response)


# Блок подсчета команд

def update_command_count(command_name):

    try:
        with open('count.json', 'r') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = {}
    except FileNotFoundError:
        data = {}

    count = data.get(command_name, 0)
    count += 1
    data[command_name] = count

    with open('count.json', 'w') as file:
        json.dump(data, file, indent=4)

    return count


# Блок проверки на админа
def is_admin(user_id):
    try:
        with open("admins.json", "r", encoding="utf-8") as f:  # Добавили encoding="utf-8"
            data = json.load(f)
            admins = data.get("admins", {})

            # Преобразуем user_id в строку для сравнения с ключами JSON
            user_id_str = str(user_id)
            return user_id_str in admins

    except FileNotFoundError:
        print("Ошибка: Файл admins.json не найден.")
        return False
    except json.JSONDecodeError:
        print("Ошибка: Неверный формат JSON в файле admins.json.")
        return False

def is_vladel_message(message):

    user_id = message.from_user.id
    return user_id == ADM

# Блок с цитатами

my_timezone = pytz.timezone('Asia/Irkutsk')

def send_message():

    with open('citates.json', 'r', encoding='utf-8') as file:
        citates = json.load(file)

    citates_list = list(citates.values())
    random_citate = random.choice(citates_list)

    message = f"{random_citate}"

    bot.send_message(chat_id, message, parse_mode='Markdown')


scheduler = BackgroundScheduler(timezone=my_timezone)

scheduler.add_job(
    send_message,
    CronTrigger(hour='12', minute='0', second='0', timezone='Asia/Irkutsk'),
    id='send_message_job'
)

scheduler.start()

# Получение айди

@bot.message_handler(commands=['id'])
def get_user_id(message):
    send_console(message)
    user_id = message.from_user.id
    if is_admin(user_id):
        if message.reply_to_message:
            user_id = message.reply_to_message.from_user.id
            bot.reply_to(message, f"✅| ID пользователя @{message.reply_to_message.from_user.username}: {user_id}")
        else:
            bot.reply_to(message, "❌| Пожалуйста, ответьте на сообщение пользователя, чей ID вы хотите узнать.")


@bot.message_handler(commands=['chatid'])
def send_chat_id(message):
    send_console(message)
    user_id = message.from_user.id
    if is_admin(user_id):
        chat_id = message.chat.id
        bot.send_message(chat_id, f"✅| Chat_id этого чата: {chat_id}")

@bot.message_handler(commands=['clear'])
def clear_cooldown(message):
    send_console(message)
    user_id = message.from_user.id
    if is_admin(user_id):
        """
        Команда для очистки кулдауна (устанавливает дату на год ранее).
        """
        # Путь к файлу с кулдаунами
        cooldown_file = 'cooldown.json'

        # Чтение данных из JSON файла
        try:
            with open(cooldown_file, 'r', encoding='utf-8') as file:
                timers = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            bot.reply_to(message, "❌|  Файл с кулдаунами не найден или поврежден.")
            return

        # Текущее время
        current_time = datetime.datetime.now()

        # Проходим по всем командам и чатам
        for game, chats in timers.items():
            for chat_id, last_used in chats.items():
                # Преобразуем строку даты в объект datetime
                last_used_time = datetime.datetime.strptime(last_used, "%Y-%m-%d %H:%M:%S")
                # Уменьшаем дату на год
                new_last_used_time = last_used_time - timedelta(days=365)
                # Обновляем значение в словаре
                timers[game][chat_id] = new_last_used_time.strftime("%Y-%m-%d %H:%M:%S")

        # Сохраняем обновленные данные обратно в файл
        with open(cooldown_file, 'w', encoding='utf-8') as file:
            json.dump(timers, file, indent=4, ensure_ascii=False)

        # Отправляем сообщение об успешной очистке
        bot.reply_to(message, "✅ Кулдауны успешно очищены")


@bot.message_handler(commands=['addadmin'])
def add_admin(message):
    send_console(message)
    user_id = message.from_user.id
    if is_admin(user_id):
        # Загружаем текущих администраторов
        try:
            with open('admins.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Проверяем, является ли data словарем
                if isinstance(data, dict):
                    admins = data.get("admins", {})
                else:
                    admins = {}  # Если это не словарь, инициализируем пустой словарь
        except (json.JSONDecodeError, ValueError):
            admins = {}  # Если произошла ошибка, инициализируем пустой словарь

        # Получаем аргументы команды
        args = message.text.split()

        if len(args) != 4:
            bot.reply_to(message, "❌| Используйте: /addadmin <user_id> <имя> <группа>\nПример: /addadmin 1746611992 Слава ИС23А")
            return

        try:
            user_id = int(args[1])  # Получаем ID
        except ValueError:
            bot.reply_to(message, "❌| Пожалуйста, введите корректный ID пользователя.")
            return

        username = args[2]  # Имя
        group = args[3]     # Группа

        # Проверяем, является ли пользователь администратором


        # Добавляем пользователя в список администраторов
        if user_id not in admins:
            admins[user_id] = f"{username} - {group}"  # Сохраняем в формате "ID - Имя - Группа"
            # Сохраняем обратно в файл в формате словаря
            data = {"admins": admins}
            with open('admins.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            bot.reply_to(message, f"✅| Пользователь {username} добавлен в администраторы с группой {group}.")
        else:
            bot.reply_to(message, f"✅| Пользователь с ID {user_id} уже является администратором.")



@bot.message_handler(commands=['removeadmin'])
def remove_admin(message):
    send_console(message)
    user_id = message.from_user.id
    if is_admin(user_id):

        try:
            with open('admins.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, dict):
                    admins = data.get("admins", {})
                else:
                    admins = {}
        except (json.JSONDecodeError, ValueError):
            admins = {}

        # Получаем аргументы команды
        args = message.text.split()

        if len(args) != 2:
            bot.reply_to(message, "❌| Используйте: /removeadmin <user_id>\nПример: /removeadmin 1746611992")
            return

        identifier = args[1]




        if identifier.isdigit():
            user_id = identifier
            if user_id in admins:
                del admins[user_id]
                bot.reply_to(message, f"✅| Администратор с ID {user_id} удалён.")
            else:
                bot.reply_to(message, f"❌| Администратор с ID {user_id} не найден.")
        else:
            bot.reply_to(message, "❌| Пожалуйста, введите корректный ID пользователя.")


        data = {"admins": admins}
        with open('admins.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

# Статистика

@bot.message_handler(func=lambda message: message.text.lower() == "статистика")
def show_statistics(message):
    send_console(message)

    # Обновляем счетчик команд
    update_command_count('статистика')

    if not check_cooldown(bot, message, 'statistika'):
        return  # Если кулдаун активен, завершаем выполнение функции

    # Чтение данных администраторов
    try:
        with open('admins.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, dict):
                admins = data.get("admins", {})
            else:
                admins = {}
    except (json.JSONDecodeError, ValueError):
        admins = {}

    response = "📊 Статистика:\n\n"

    if admins:
        response += "👑 Администраторы:\n"
        for user_id, info in admins.items():
            response += f"   🆔 {user_id} | 👤 {info}\n"



    else:
        response += "   ❌| Администраторы не найдены.\n"

    # Чтение данных по использованию команд
    try:
        with open('count.json', 'r', encoding='utf-8') as f:
            counts = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        counts = {}

    if counts:
        response2 = "\n📈 Использование команд:\n\n"
        for command, count in counts.items():
            response2 += f"   ⚙️ {command}: {count}\n"
        response2 += f"\n\n✏️ Число строк в боте\n\n🧓 ИС23а (16ноя 2024) рассчитанный на одну группу (v1) - 439\n\n👦 GroupSchedBot (16 февраля 2025) расчитанный на большое количество групп (v2) - 1310"

    else:
        response2 = "\n   ❌| Нет данных по использованию команд.\n"

    # Отправляем ответ пользователю
    bot.reply_to(message, response)
    bot.reply_to(message, response2)


@bot.message_handler(commands=['расписание'])
def schedule_command(message):
    send_console(message)

    user_id = message.from_user.id
    if is_admin(user_id):
        chat_id = message.chat.id

        # Создаем инлайн-кнопки
        markup = types.InlineKeyboardMarkup()

        template_button = types.InlineKeyboardButton("Шаблон", callback_data='template')
        custom_button = types.InlineKeyboardButton("Кастом", callback_data='custom')

        markup.add(template_button, custom_button)

        # Отправляем сообщение с кнопками
        bot.send_message(chat_id,
                         "👷‍♂️Мастер настройки расписания запущен.\n\n"
                         "📃Шаблон - готовый шаблон расписания, делаете по инструкции.\n\n"
                         "✏️Кастом - Ваш стиль расписания, отправляете готовый текст, чтобы бот его сохранил.\n\nP.S. перезарядка кнопок - 15сек.",
                         reply_markup=markup)
        update_command_count('/расписание')


# Мастер старта

@bot.message_handler(commands=['start'])
def send_welcome(message):
    send_console(message)
    markup = types.InlineKeyboardMarkup()



    add_bot_button = types.InlineKeyboardButton("Добавить❓", callback_data='add_bot')
    status_button = types.InlineKeyboardButton("Статус📃", callback_data='status')


    markup.add(add_bot_button, status_button)

    welcome_text = (
        "Привет! 👋\n"
        "Вы вызвали мастера установки бота.\n"
        "Выберите кнопку ниже для решения вашего вопроса."
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)
    update_command_count('/start')


@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    chat_id = call.message.chat.id

    # Обработка различных callback_data
    if call.data == 'add_bot':
        game = 'add_bot'  # Название команды, которую мы обрабатываем

        # Проверка кулдауна
        if not check_cooldown_call(bot, call.message, game):
            return  # Если кулдаун активен, ничего не отправляем
        handle_add_bot(chat_id)

    elif call.data == 'status':
        game = 'status'  # Название команды, которую мы обрабатываем

        # Проверка кулдауна
        if not check_cooldown_call(bot, call.message, game):
            return  # Если кулдаун активен, ничего не отправляем

        try:
            with open('podpiska.json', 'r', encoding='utf-8') as f:
                data = json.load(f)

            user_data = data.get(str(chat_id))
            if user_data:
                status = user_data.get("status")
                expiry_date_str = user_data.get("expiry_date")

                if status == "active" and expiry_date_str:
                    expiry_date = datetime.datetime.strptime(expiry_date_str, "%Y-%m-%d")
                    current_date = datetime.datetime.now()

                    if current_date <= expiry_date:
                        remaining_time = expiry_date - current_date
                        days_remaining = remaining_time.days
                        hours_remaining = remaining_time.seconds // 3600
                        minutes_remaining = (remaining_time.seconds // 60) % 60

                        message = (f"✅| Ваша подписка активна.\n"
                                   f"Осталось: {days_remaining} дн. {hours_remaining} ч. {minutes_remaining} мин.")
                    else:
                        message = "❌| Ваша подписка истекла."
                else:
                    message = "❌| Ваша подписка неактивна."
            else:
                message = ("❌| Статус подписки не найден.\n\n"
                           "Возможно вы не покупали подписку никогда ранее. Для этого оплатите подписку.")
        except Exception as e:
            message = f"❌| Произошла ошибка: {str(e)}"

        # Отправляем сообщение пользователю
        bot.send_message(chat_id, message)

    elif call.data == 'template':
        game = 'template'  # Название команды, которую мы обрабатываем

        # Проверка кулдауна
        if not check_cooldown_call(bot, call.message, game):
            return  # Если кулдаун активен, ничего не отправляем
        user_id = call.from_user.id
        if is_admin(user_id):
            handle_template(call)
    elif call.data == 'custom':
        game = 'custom'  # Название команды, которую мы обрабатываем

        # Проверка кулдауна
        if not check_cooldown_call(bot, call.message, game):
            return  # Если кулдаун активен, ничего не отправляем
        handle_custom(chat_id)
    elif call.data == 'set_schedule':
        game = 'set_schedule'  # Название команды, которую мы обрабатываем

        # Проверка кулдауна
        if not check_cooldown_call(bot, call.message, game):
            return  # Если кулдаун активен, ничего не отправляем
        user_id = call.from_user.id
        if is_admin(user_id):
            handle_set_schedule(call)
    elif call.data == 'end_schedule':
        game = 'end_schedule'  # Название команды, которую мы обрабатываем

        # Проверка кулдауна
        if not check_cooldown_call(bot, call.message, game):
            return  # Если кулдаун активен, ничего не отправляем
        user_id = call.from_user.id
        if is_admin(user_id):
            handle_end_schedule(chat_id)
    elif call.data == 'del_schedule':
        game = 'del_schedule'  # Название команды, которую мы обрабатываем

        # Проверка кулдауна
        if not check_cooldown_call(bot, call.message, game):
            return  # Если кулдаун активен, ничего не отправляем
        user_id = call.from_user.id
        if is_admin(user_id):
            handle_del_schedule(call)
    elif call.data == 'add_another':
        game = 'add_another'  # Название команды, которую мы обрабатываем

        # Проверка кулдауна
        if not check_cooldown_call(bot, call.message, game):
            return  # Если кулдаун активен, ничего не отправляем
        user_id = call.from_user.id
        if is_admin(user_id):
            handle_add_another(call)
    elif call.data == 'red_schedule':
        game = 'red_schedule'  # Название команды, которую мы обрабатываем

        # Проверка кулдауна
        if not check_cooldown_call(bot, call.message, game):
            return  # Если кулдаун активен, ничего не отправляем
        user_id = call.from_user.id
        if is_admin(user_id):
            handle_red_schedule(call)

def handle_add_bot(chat_id):
    bot.send_message(chat_id, "*Инструкции по добавлению бота*\n\n"
                               "1. 🧑‍⚖️Написать _Владельцу_ (@slepta)️\n\n"
                               "2. 📃Добавить бота в беседу _ОБЯЗАТЕЛЬНО в администраторы_ (права нужны для корректной работы)\n\n"
                               "3. 🤖Добавить временно владельца @slepta для настройки бота\n\n"
                               "4. 💵Вы получите **БЕСПЛАТНО** временную подписку на неделю. По истечению которой если вас всё устраивает - оплатить **ПОДПИСКУ**\n\n"
                               "P.S. оплата в лс у @slepta",
                               parse_mode='Markdown')

def handle_template(call):
    bot.answer_callback_query(call.id, "Вы выбрали шаблон расписания.")
    bot.send_message(call.message.chat.id,
                     "Пример шаблона расписания:\n\n"
                     "🕰13:40-14:50 📗1н МДК 03.01 | 212\n2н МДК 02.02 | 212\n"
                     "🕰14:55-16:05 📗 Философия | 216\n"
                     "🕰16:25-17:35 📗 МДК 02.03 | 214а\n"
                     "🕰17:40-18:50 📗 Физ-ра | з/зал\n\nКнопки работают только у Адм.👑\n"
                     "\n‼️‼️‼️ВНИМАНИЕ\nна время настройки расписания, никто лишний в чат писать не должен! Иначе бот будет неккоректно записывать данные.\n\n(команда) Статистика отправляет список админов и еще интересной инфы)"
                     )
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Добавить пару", callback_data='set_schedule'))
    markup.add(types.InlineKeyboardButton("Удалить пару", callback_data='del_schedule'))
    markup.add(types.InlineKeyboardButton("Изменить пару", callback_data='red_schedule'))
    bot.send_message(call.message.chat.id, "Выберите действие:", reply_markup=markup)

def handle_custom(chat_id):
    bot.send_message(chat_id, "❌| в разработке (наверное)")


def handle_set_schedule(call):
    chat_id = call.message.chat.id

    bot.send_message(chat_id, "❓| Введите время пары (например, 13:40-14:50):")

    # Регистрация следующего шага с передачей данных (в данном случае чата)
    bot.register_next_step_handler(call.message, get_subject, chat_id)

def handle_end_schedule(chat_id):
    bot.send_message(chat_id, "✅| Работа с парами завершена. Если вам нужно что-то еще, просто напишите /расписание!")

def handle_del_schedule(call):  # Изменяем параметр на call
    chat_id = call.message.chat.id
    bot.send_message(chat_id, "❓| Введите день недели (сокращенно):\nПн - понедельник\nВт - вторник\nСр - среда\nЧт - четверг\nПт - пятница\nСб - суббота\nВс - воскресенье:")
    bot.register_next_step_handler(call.message, ask_for_pair_number, chat_id)

def handle_add_another(call):  # Изменяем параметр на call
    chat_id = call.message.chat.id  # Извлекаем chat_id из call
    bot.send_message(chat_id, "❓| Введите время пары (например, 13:40-14:50):")
    bot.register_next_step_handler(call.message, get_subject, chat_id)

def handle_red_schedule(call):
    chat_id = call.message.chat.id
    bot.send_message(chat_id, "❓| Введите день недели (сокращенно):\nПн - понедельник\nВт - вторник\nСр - среда\nЧт - четверг\nПт - пятница\nСб - суббота\nВс - воскресенье:")
    bot.register_next_step_handler(call.message, ask_for_pair_to_edit, chat_id)

def ask_for_pair_to_edit(message, chat_id):
    day = message.text.lower().strip()
    print(f"Пользователь ввел день: {day}")  # Для отладки

    # Приводим chat_id к строке для соответствия ключам
    str_chat_id = str(chat_id)

    # Проверяем, является ли введенное сокращение допустимым
    if day in days_mapping:
        full_day = days_mapping[day]  # Получаем полное название дня
    else:
        bot.send_message(chat_id, "❌| Неверный день недели. Пожалуйста, используйте сокращения: Пн, Вт, Ср, Чт, Пт, Сб, Вс.")
        return

    if str_chat_id in calendar:
        if full_day in calendar[str_chat_id]:
            pairs = calendar[str_chat_id][full_day]
            print(f"Пары на день {full_day}: {pairs}")  # Для отладки
            if pairs:
                response = "Выберите пару для изменения:\n"
                for index, pair in enumerate(pairs, start=1):
                    response += f"{index}. {pair}\n"
                bot.send_message(chat_id, response + "Введите номер пары для изменения:")
                bot.register_next_step_handler(message, edit_pair, full_day, str_chat_id)
            else:
                bot.send_message(chat_id, "❌| У вас нет пар на этот день.")
        else:
            bot.send_message(chat_id, "❌| Неверный день недели или у вас нет расписания на этот день.")
    else:
        bot.send_message(chat_id, "❌| Расписание не найдено для данного пользователя.")
def edit_pair(message, day, chat_id):
    try:
        # Получаем номер пары и изменяем соответствующий элемент
        pair_number = int(message.text) - 1
        if chat_id in calendar and day in calendar[chat_id]:
            pairs = calendar[chat_id][day]
            if 0 <= pair_number < len(pairs):
                # Отправляем информацию о текущей паре
                current_pair = pairs[pair_number]
                bot.send_message(chat_id, f"❓| Текущая пара: {current_pair}\nВведите новое время пары (например, 13:40-14:50):")
                bot.register_next_step_handler(message, get_new_subject, pair_number, day, chat_id)
            else:
                bot.send_message(chat_id, "❌| Неверный номер пары.")
        else:
            bot.send_message(chat_id, "❌| Расписание не найдено.")
    except ValueError:
        bot.send_message(chat_id, "❌| Пожалуйста, введите корректный номер пары.")

def get_new_subject(message, pair_number, day, chat_id):
    new_time = message.text
    bot.send_message(chat_id, "❓| Введите новое название пары (кратко):")
    bot.register_next_step_handler(message, finalize_edit, pair_number, day, new_time, chat_id)

def finalize_edit(message, pair_number, day, new_time, chat_id):
    new_subject = message.text
    bot.send_message(chat_id, "❓| Введите новый номер кабинета:")
    bot.register_next_step_handler(message, update_schedule, pair_number, day, new_time, new_subject, chat_id)

def update_schedule(message, pair_number, day, new_time, new_subject, chat_id):
    new_room = message.text
    new_entry = f"🕰{new_time} 📗{new_subject} | {new_room}"

    # Обновляем запись в расписании
    calendar[chat_id][day][pair_number] = new_entry  # Изменяем запись
    save_calendar(calendar)  # Сохраняем изменения

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Добавить", callback_data='add_another'),
               types.InlineKeyboardButton("Изменить", callback_data='red_schedule'),
               types.InlineKeyboardButton("Удалить", callback_data='del_schedule'),
               types.InlineKeyboardButton("Конец", callback_data='end_schedule'))
    bot.send_message(chat_id, "✅| Пара изменена! Хотите выполнить еще действие?", reply_markup=markup)

def ask_for_pair_number(message, chat_id):
    day = message.text.lower().strip()

    # Приводим chat_id к строке для соответствия ключам
    str_chat_id = str(chat_id)

    # Проверяем, является ли введенное сокращение допустимым
    if day in days_mapping:
        full_day = days_mapping[day]  # Получаем полное название дня
    else:
        bot.send_message(chat_id, "❌| Неверный день недели. Пожалуйста, используйте сокращения: Пн, Вт, Ср, Чт, Пт, Сб, Вс.")
        return

    # Проверяем, существует ли расписание для данного chat_id
    if str_chat_id in calendar and full_day in calendar[str_chat_id]:
        pairs = calendar[str_chat_id][full_day]
        if pairs:
            # Формируем список пар для отображения
            response = "Выберите пару для удаления:\n"
            for index, pair in enumerate(pairs, start=1):
                response += f"{index}. {pair}\n"
            bot.send_message(chat_id, response + "Введите номер пары для удаления:")
            bot.register_next_step_handler(message, delete_pair, full_day, str_chat_id)
        else:
            bot.send_message(chat_id, "❌| У вас нет пар на этот день.")
    else:
        bot.send_message(chat_id, "❌| Неверный день недели или у вас нет расписания на этот день.")

def delete_pair(message, day, chat_id):
    try:
        # Получаем номер пары и удаляем соответствующий элемент
        pair_number = int(message.text) - 1
        if chat_id in calendar and day in calendar[chat_id]:
            pairs = calendar[chat_id][day]
            if 0 <= pair_number < len(pairs):
                deleted_pair = pairs.pop(pair_number)  # Удаляем пару
                save_calendar(calendar)  # Сохраняем изменения
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton("Добавить", callback_data='add_another'),
                           types.InlineKeyboardButton("Изменить", callback_data='red_schedule'),
                           types.InlineKeyboardButton("Удалить", callback_data='del_schedule'),
                           types.InlineKeyboardButton("Конец", callback_data='end_schedule'))
                bot.send_message(chat_id, f"✅| Пара {deleted_pair} удалена! Хотите еще выполнить действия?", reply_markup=markup)
            else:
                bot.send_message(chat_id, "❌| Неверный номер пары.")
        else:
            bot.send_message(chat_id, "❌| Расписание не найдено.")
    except ValueError:
        bot.send_message(chat_id, "❌| Пожалуйста, введите корректный номер пары.")

def get_subject(message, chat_id):
    time = message.text
    bot.send_message(chat_id, "❓| Введите название пары (кратко):")
    bot.register_next_step_handler(message, get_room, time, chat_id)

def get_room(message, time, chat_id):
    subject = message.text
    bot.send_message(chat_id, "❓| Введите номер кабинета:")
    bot.register_next_step_handler(message, finalize_schedule, time, subject, chat_id)

def finalize_schedule(message, time, subject, chat_id):
    room = message.text
    entry = f"🕰{time} 📗{subject} | {room}"

    # Запрашиваем день недели
    bot.send_message(chat_id, "❓| Введите день недели (сокращенно):\nПн - понедельник\nВт - вторник\nСр - среда\nЧт - четверг\nПт - пятница\nСб - суббота\nВс - воскресенье:")
    bot.register_next_step_handler(message, add_entry, entry, chat_id)

def add_entry(message, entry, chat_id):
    day = message.text.lower().strip()

    # Приводим chat_id к строке для соответствия ключам
    str_chat_id = str(chat_id)

    # Проверяем, существует ли расписание для данного chat_id
    if str_chat_id not in calendar:
        # Если расписания нет, создаем новый словарь для этого chat_id
        calendar[str_chat_id] = {
            "monday": [],
            "tuesday": [],
            "wednesday": [],
            "thursday": [],
            "friday": [],
            "saturday": [],
            "sunday": []
        }

    # Проверяем, является ли введенное сокращение допустимым
    if day in days_mapping:
        full_day = days_mapping[day]  # Получаем полное название дня
    else:
        bot.send_message(chat_id, "❌| Неверный день недели. Пожалуйста, используйте сокращения: Пн, Вт, Ср, Чт, Пт, Сб, Вс.")
        return  # Выходим из функции, если день некорректный

    # Добавляем новую запись в существующий список
    calendar[str_chat_id][full_day].append(entry)  # Добавляем запись в список

    # Сохраняем расписание
    save_calendar(calendar)

    # Предлагаем добавить еще одну пару или закончить
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Добавить", callback_data='add_another'),  types.InlineKeyboardButton("Изменить", callback_data='red_schedule'), types.InlineKeyboardButton("Удалить", callback_data='del_schedule') , types.InlineKeyboardButton("Конец", callback_data='end_schedule'))
    bot.send_message(chat_id, "✅| Пара добавлена! Хотите добавить еще одну?", reply_markup=markup)



# Команда статус для проверки подписки

@bot.message_handler(func=lambda message: message.text.lower() == "статус")
def check_status(message):
    send_console(message)
    if not check_cooldown(bot, message, 'status'):
        return  # Если кулдаун активен, завершаем выполнение функции
    chat_id = message.chat.id
    update_command_count('статус')
    try:
        with open('podpiska.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        user_data = data.get(str(chat_id))
        if user_data:
            status = user_data.get("status")
            expiry_date_str = user_data.get("expiry_date")

            if status == "active" and expiry_date_str:
                expiry_date = datetime.datetime.strptime(expiry_date_str, "%Y-%m-%d")
                current_date = datetime.datetime.now()

                if current_date <= expiry_date:
                    remaining_time = expiry_date - current_date
                    days_remaining = remaining_time.days
                    hours_remaining = remaining_time.seconds // 3600
                    minutes_remaining = (remaining_time.seconds // 60) % 60

                    bot.send_message(chat_id,
                                     f"✅| Ваша подписка активна.\n"
                                     f"Осталось: {days_remaining} дн. {hours_remaining} ч. {minutes_remaining} мин.")
                else:
                    bot.send_message(chat_id, "❌| Ваша подписка истекла.")
            else:
                bot.send_message(chat_id, "❌| Ваша подписка неактивна.")
        else:
            bot.send_message(chat_id, "❌| Статус подписки не найден.\n\nВозможно вы не покупали подписку никогда ранее. Для этого оплатите подписку.")

    except FileNotFoundError:
        bot.send_message(chat_id, "❌| Ошибка: файл подписки не найден.")
    except json.JSONDecodeError:
        bot.send_message(chat_id, "❌| Ошибка: не удалось прочитать данные из файла.")
    except Exception as e:
        bot.send_message(chat_id, f"❌| Произошла ошибка: {str(e)}")

# Команда старта подписки по чат айди

@bot.message_handler(func=lambda message: message.text.startswith('Старт (') and message.text.endswith(')'))
def start_subscription(message):
    send_console(message)
    chat_id = message.chat.id
    if is_vladel_message(message):
        chat_id_str = message.text[7:-1]

        try:
            chat_id = int(chat_id_str)
        except ValueError:
            bot.send_message(message.chat.id, "Неверный формат chat_id.")
            return

        # Устанавливаем дату окончания подписки на 1 месяц
        expiry_date = datetime.datetime.now() + datetime.timedelta(days=30)
        expiry_date_str = expiry_date.strftime("%Y-%m-%d")

        try:

            with open('podpiska.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {}
        except json.JSONDecodeError:
            data = {}

        data[str(chat_id)] = {
            "status": "active",
            "expiry_date": expiry_date_str
        }

        with open('podpiska.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        bot.send_message(message.chat.id, f"✅| Подписка выдана для группы с айди: {chat_id}.")
    else:
        bot.send_message(chat_id, "❌| Кажется, ты не владелец)")


@bot.message_handler(commands=['s'])
def write_roles_handler(message):
    send_console(message)

    if message.from_user.id == ADM:

        if message.text.lower().startswith('/s'):

            text = message.text[len('/s'):].strip()

            if len(text) > 0:

                with open('send.json', 'w') as file:
                    data = {
                        'sms': text
                    }
                    json.dump(data, file)

            with open('send.json', 'r', encoding='utf-8') as json_file:
                data = json.load(json_file)

            bot.send_message(chat_id, f"{data['sms']}")

# Фан-команда с рандомными голосовыми

@bot.message_handler(func=lambda message: message.text.lower() == 'рандом')
def random_voice(message):
    send_console(message)
    if not check_cooldown(bot, message, 'random'):
        return  # Если кулдаун активен, завершаем выполнение функции
    update_command_count('рандом')
    chat_id = message.chat.id  # Получаем chat_id из сообщения

    with open('podpiska.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    user_data = data.get(str(chat_id))
    if user_data:
        status = user_data.get("status")
        expiry_date_str = user_data.get("expiry_date")

        if status == "active" and expiry_date_str:
            expiry_date = datetime.datetime.strptime(expiry_date_str, "%Y-%m-%d")
            current_date = datetime.datetime.now()

            if current_date <= expiry_date:
                current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                game = "random"
                with open('cooldown.json', 'r') as file:
                    timers = json.load(file)

                if str(game) in timers:
                    last_time = datetime.datetime.strptime(timers[str(game)], "%Y-%m-%d %H:%M:%S")

                    time_difference = datetime.datetime.now() - last_time

                    if time_difference.total_seconds() < 10:

                        remaining_time = datetime.timedelta(seconds=10 - time_difference.total_seconds())

                        remaining_time_datetime = datetime.datetime(1, 1, 1) + remaining_time

                        bot.reply_to(message, text=f'❌| Кулдаун! Осталось времени: {remaining_time_datetime.strftime("%M:%S")} секунд' )

                        pass

                        return
                timers[str(game)] = current_time
                with open('cooldown.json', 'w') as file:
                    json.dump(timers, file)

                music_folder = "musicrand"

                music_files = os.listdir(music_folder)

                random_music = random.choice(music_files)

                music_path = os.path.join(music_folder, random_music)

                chat = message.chat.id

                with open(music_path, 'rb') as music:
                    bot.send_audio(chat, music)
            else:
                bot.send_message(chat_id, "❌| Ваша подписка истекла.")
        else:
            bot.send_message(chat_id, "❌| Ваша подписка неактивна.")
    else:
        bot.send_message(chat_id,
                         "❌| Статус подписки не найден.\n\nВозможно вы не покупали подписку никогда ранее. Для этого оплатите подписку.")

# Команда для проверки состояния бота

@bot.message_handler(func=lambda message: message.text.lower() == "бот")
def handle_bot_command(message):
    send_console(message)
    update_command_count('бот')
    if not check_cooldown(bot, message, 'bot'):
        return  # Если кулдаун активен, завершаем выполнение функции
    bot.send_message(message.chat.id, text='✅| На месте')



# Команда с выводом расписания

@bot.message_handler(func=lambda message: message.text.lower() == "расписание недели")
def send_week_schedule(message):
    send_console(message)
    update_command_count('расписание недели')
    if not check_cooldown(bot, message, 'raspisaniefull'):
        return  # Если кулдаун активен, завершаем выполнение функции

    chat_id = message.chat.id  # Получаем chat_id из сообщения

    with open('podpiska.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    user_data = data.get(str(chat_id))
    if user_data:
        status = user_data.get("status")
        expiry_date_str = user_data.get("expiry_date")

        if status == "active" and expiry_date_str:
            expiry_date = datetime.datetime.strptime(expiry_date_str, "%Y-%m-%d")
            current_date = datetime.datetime.now()

            if current_date <= expiry_date:

                with open('calendar.json', 'r', encoding='utf-8') as file:
                    schedule_data = json.load(file)

                reply_text = "🧠| Расписание на неделю:\n"

                days_order = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
                for i in range(7):
                    day = days_order[i]
                    day_ru = days_of_week.get(day)
                    daily_schedule = schedule_data.get(str(chat_id), {}).get(day, [])
                    reply_text += f"\n\n🔥| {day_ru}:\n" + "\n".join(
                        daily_schedule) if daily_schedule else f"\n\n📅| Расписание на {day_ru.lower()} отсутствует.\n\n"

                bot.reply_to(message, reply_text)

                with open('zameni.json', 'r', encoding='utf-8') as file:
                    zameni = json.load(file)
                bot.reply_to(message, text=f"\n\n⁉️| ЗАМЕНЫ\n\n✅| {zameni.get('zam', 'Нет замен.')}")
            else:
                bot.send_message(chat_id, "❌| Ваша подписка истекла.")
        else:
            bot.send_message(chat_id, "❌| Ваша подписка неактивна.")
    else:
        bot.send_message(chat_id,
                         "❌| Статус подписки не найден.\n\nВозможно вы не покупали подписку никогда ранее. Для этого оплатите подписку.")

@bot.message_handler(func=lambda message: message.text.lower() == "расписание все")
def handle_all_schedule_command(message):
    send_console(message)
    if not check_cooldown(bot, message, 'raspisanieold'):
        return  # Если кулдаун активен, завершаем выполнение функции
    bot.reply_to(message, "📢| Команда переехала - используйте 'расписание недели' для получения расписания на всю неделю.")

# Команда с выводом расписания

@bot.message_handler(func=lambda message: message.text.lower() == "расписание")
def send_schedule1(message):
    send_console(message)
    update_command_count('расписание')
    if not check_cooldown(bot, message, 'raspisanie'):
        return  # Если кулдаун активен, завершаем выполнение функции
    chat_id = message.chat.id

    with open('podpiska.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    user_data = data.get(str(chat_id))
    if user_data:
        status = user_data.get("status")
        expiry_date_str = user_data.get("expiry_date")

        if status == "active" and expiry_date_str:
            expiry_date = datetime.datetime.strptime(expiry_date_str, "%Y-%m-%d")
            current_date = datetime.datetime.now()

            if current_date <= expiry_date:
                current_time = datetime.datetime.now(my_timezone)
                current_timee = current_time.strftime("%Y-%m-%d %H:%M:%S")
                game = "main"    # конец проверки на подписку

                current_date = datetime.datetime.now(tz=my_timezone)

                if current_date.hour == 0 and current_date.minute == 0:
                    current_date += datetime.timedelta(days=1)

                current_weekday = current_date.strftime("%A").lower()
                current_weekday_ru = days_of_week.get(current_weekday)

                if current_weekday_ru is None:
                    print("❌| Не удалось определить день недели.")
                else:
                    current_date_day = current_date.strftime("%d")
                    current_date_month = months_of_year[current_date.strftime("%m")]

                    reply_text = f"🔥| День: {current_weekday_ru}\n🥵| Число: {current_date_day} {current_date_month}"

                    with open('calendar.json', 'r', encoding='utf-8') as file:
                        schedule_data = json.load(file)

                    daily_schedule = schedule_data.get(str(chat_id), {}).get(current_weekday, [])
                    reply_text += "\n\n" + "\n".join(daily_schedule) if daily_schedule else "\n\n📅| Расписание на сегодня отсутствует."

                    next_day = current_date + datetime.timedelta(days=1)
                    next_weekday = next_day.strftime("%A").lower()
                    next_weekday_ru = days_of_week.get(next_weekday)
                    next_day_schedule = schedule_data.get(str(chat_id), {}).get(next_weekday, [])

                    reply_text += f"\n\n👉| НА ЗАВТРА: {next_weekday_ru}\n\n" + "\n".join(next_day_schedule) if next_day_schedule else "\n\n📅| Расписание на завтра отсутствует."

                bot.reply_to(message, reply_text)

                # Получение замен для конкретного чата
                try:
                    with open('zameni.json', 'r', encoding='utf-8', errors='ignore') as file:
                        zameni = json.load(file)
                    chat_replacements = zameni.get(str(chat_id), {}).get('text', 'Нет замен.')
                    bot.reply_to(message, text=f"\n\n⁉️| ЗАМЕНЫ\n\n✅| {chat_replacements}")
                except FileNotFoundError:
                    bot.reply_to(message, text='❌| Файл zameni.json не найден.')
                except json.JSONDecodeError:
                    bot.reply_to(message, text='❌| Ошибка при чтении файла zameni.json.')
            else:
                bot.send_message(chat_id, "❌| Ваша подписка истекла.")
        else:
            bot.send_message(chat_id, "❌| Ваша подписка неактивна.")
    else:
        bot.send_message(chat_id,
                         "❌| Статус подписки не найден.\n\nВозможно вы не покупали подписку никогда ранее. Для этого оплатите подписку.")



# Команда для записи замен

@bot.message_handler(commands=['замены'])
def write_commands(message):
    send_console(message)
    update_command_count('/замены')
    user_id = message.from_user.id
    chat_id = message.chat.id  # Получаем ID чата

    if is_admin(user_id):
        if message.text.lower().startswith('/замены'):
            text = message.text[len('/замены'):].strip()

            if len(text) > 0:
                # Загружаем существующие данные из zameni.json, если файл существует
                try:
                    with open('zameni.json', 'r', encoding='utf-8') as file:
                        data = json.load(file)
                except FileNotFoundError:
                    data = {}
                except json.JSONDecodeError:
                    # Если возникла ошибка декодирования, создаем пустой словарь
                    data = {}
                except Exception as e:
                    print(f"Ошибка при чтении файла: {e}")
                    data = {}

                # Добавляем или обновляем запись для текущего чата
                data[str(chat_id)] = {
                    "text": text
                }

                # Записываем обновленные данные обратно в файл
                with open('zameni.json', 'w', encoding='utf-8') as file:
                    json.dump(data, file, ensure_ascii=False, indent=4)

                response = '✅| Поле с заменами обновлено'
                bot.reply_to(message, response)

            else:
                response = '❌| Вы не ввели текст для обновления поля с заменами'
                bot.reply_to(message, response)



if __name__ == '__main__':
    bot.delete_webhook(drop_pending_updates=True)
    bot.infinity_polling()
