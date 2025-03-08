# Telegram Schedule Bot

---

## Описание бота

Этот Telegram-бот предназначен для управления расписанием занятий, замен и других учебных событий. Бот поддерживает команды для пользователей и администраторов, позволяя просматривать расписание, настраивать его, а также выполнять дополнительные функции, такие как проверка статуса подписки, статистика и рандомные звуки.

---

## Команды

### Основные команды:

#### Пользовательские команды (просто текст):
- **Расписание** — Показывает расписание на текущий и следующий день.
- **Расписание недели** — Показывает расписание на всю неделю.
- **Статус** — Выводит статус вашей подписки.
- **Статистика** — Показывает интересную статистику.
- **Рандом** — Отправляет рандомный звук в виде голосового сообщения.
- **Бот** — Проверяет активность бота.

#### Технические команды (только для админов, через `/`):
- **/расписание** — Настройка расписания (добавить, удалить, изменить пару).
- **/замены** — Мини-поле для ввода замен (если такие имеются).
- **/clear** — Очищает перезарядку всех команд.
- **/addadmin id (имя комментарий)** — Добавляет администратора. Пример: `/addadmin 1111 Слава 2ИС23а`.
- **/removeadmin id** — Удаляет администратора.
- **/chatid** — Показывает ID чата.
- **/id** (ответить на сообщение пользователя) — Показывает ID пользователя.
- **Старт (chat_id)** — Запускает подписку бота на 1 месяц в указанном чате (только для админов).

---

## Важные примечания

- **Недосчет:** При настройке расписания бот принимает любые сообщения (даже случайные, например, "всем привет"). Пожалуйста, будьте терпеливы и просите всех в чате не писать во время настройки расписания.
- **Подписка:** Некоторые функции доступны только при активной подписке. Проверить статус подписки можно командой **Статус**.

---

## Как использовать

1. Добавьте бота в ваш чат.
2. Используйте команды для управления расписанием и другими функциями.
3. Для администрирования используйте технические команды, доступные только администраторам.

---

## Установка и запуск

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/BymBu/GroupShedBot-telegram.git

Install dependencies:

1. pip install -r requirements.txt

Run the bot:
1. python bot.py

# Telegram Schedule Bot

---

## Bot Description

This Telegram bot is designed to manage class schedules, substitutions, and other academic events. The bot supports commands for both users and administrators, allowing you to view schedules, configure them, and perform additional functions such as checking subscription status, viewing statistics, and playing random sounds.

---

## Commands

### Main Commands:

#### User Commands (plain text):
- **Schedule** — Shows the schedule for the current and next day.
- **Weekly Schedule** — Shows the schedule for the entire week.
- **Status** — Displays your subscription status.
- **Statistics** — Shows interesting statistics.
- **Random** — Sends a random sound as a voice message.
- **Bot** — Checks the bot's activity.

#### Technical Commands (admin-only, via `/`):
- **/schedule** — Configure the schedule (add, remove, or modify a class).
- **/substitutions** — A mini-field for entering substitutions (if any).
- **/clear** — Clears the cooldown for all commands.
- **/addadmin id (name comment)** — Adds an admin. Example: `/addadmin 1111 Slava 2IS23a`.
- **/removeadmin id** — Removes an admin.
- **/chatid** — Displays the chat ID.
- **/id** (reply to a user's message) — Displays the user's ID.
- **Start (chat_id)** — Activates a 1-month subscription for the bot in the specified chat (admin-only).

---

## Important Notes

- **Drawback:** When configuring the schedule, the bot accepts any messages (even random ones like "hello everyone"). Please be patient and ask everyone in the chat to remain silent during the setup process.
- **Subscription:** Some features are only available with an active subscription. Check your subscription status using the **Status** command.

---

## How to Use

1. Add the bot to your chat.
2. Use the commands to manage the schedule and other functions.
3. For administration, use the technical commands available only to admins.

---


Install dependencies:

1. pip install -r requirements.txt

Run the bot:
1. python bot.py

## Installation and Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/BymBu/GroupShedBot-telegram.git
