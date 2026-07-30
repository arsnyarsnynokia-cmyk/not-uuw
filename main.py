import os
import time
import telebot
from telebot import types

# 1. Получаем токены из переменных окружения
BOT_TOKEN = os.environ.get('BOT_TOKEN')
ADMIN_ID = 7771113861

# 2. Инициализируем бота
bot = telebot.TeleBot(BOT_TOKEN)


# Вспомогательная функция для уведомления админа
def notify_admin(user, action_text):
    if ADMIN_ID:
        username = f"@{user.username}" if user.username else "Без юзернейма"
        report = (
            f"🔔 **Действие в боте!**\n\n"
            f"👤 **Пользователь:** {user.first_name} ({username})\n"
            f"🆔 **ID:** `{user.id}`\n"
            f"📌 **Действие:** {action_text}"
        )
        try:
            bot.send_message(ADMIN_ID, report, parse_mode="Markdown")
        except Exception as e:
            print(f"Ошибка при отправке уведомления админу: {e}")


# Команда /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    try:
        user = message.from_user
        notify_admin(user, "Запустил бота (/start)")

        markup = types.InlineKeyboardMarkup(row_width=1)
        btn_ref = types.InlineKeyboardButton(
            text="💳 Оформить бизнес-карту", url="https://vt.tiktok.com/ZS4eNAsBS/"
        )
        btn_done = types.InlineKeyboardButton(
            text="✅ Карта оформлена", callback_data="card_done"
        )
        btn_contact = types.InlineKeyboardButton(
            text="💬 Связаться с нами", url="https://t.me/livernu_colbas"
        )

        markup.add(btn_ref, btn_done, btn_contact)

        welcome_text = (
            f"Привет, {user.first_name}! 👋\n\n"
            "Я твой персональный **Бизнес-Ассистент**.\n\n"
            "Помогаю оформить бизнес-карту, а также могу передать твои вопросы менеджеру — "
            "просто напиши свое сообщение в чат! 👇"
        )

        bot.send_message(
            message.chat.id, welcome_text, reply_markup=markup, parse_mode="Markdown"
        )
    except Exception as e:
        print(f"Ошибка в /start: {e}")


# Обработка кнопки «Карта оформлена»
@bot.callback_query_handler(func=lambda call: call.data == "card_done")
def handle_card_done(call):
    try:
        user = call.from_user
        notify_admin(user, "Нажал кнопку «Карта оформлена»")
        
        try:
            bot.answer_callback_query(call.id)
        except Exception:
            pass

        response_text = (
            "Отлично! Ваша заявка принята на проверку банком (она занимает от 14 до"
            " 30 дней).\n\n"
            "Пожалуйста, пришлите в ответ на это сообщение ваш номер телефона, который"
            " вы указывали при оформлении."
        )
        bot.send_message(call.message.chat.id, response_text)
    except Exception as e:
        print(f"Ошибка в handle_card_done: {e}")


# Команда админа для ответа: /reply ID Текст
@bot.message_handler(commands=['reply'])
def reply_to_user(message):
    try:
        if message.from_user.id != ADMIN_ID:
            return

        parts = message.text.split(maxsplit=2)
        if len(parts) < 3:
            bot.reply_to(
                message,
                "⚠️ **Формат:** `/reply ID_пользователя Текст`",
                parse_mode="Markdown",
            )
            return

        target_id = int(parts[1])
        text_to_send = parts[2]

        bot.send_message(
            target_id,
            f"💬 **Ответ от администратора:**\n\n{text_to_send}",
            parse_mode="Markdown",
        )
        bot.reply_to(message, "✅ **Сообщение отправлено!**")
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: `{e}`", parse_mode="Markdown")


# Обработка обычных сообщений (вопросы клиентов и номера телефонов)
@bot.message_handler(content_types=['text'])
def handle_text(message):
    try:
        user = message.from_user

        # 1. Если пишет админ (и это не команда /reply), ничего не делаем
        if user.id == ADMIN_ID:
            return

        # 2. Уведомляем тебя в личку о полученном сообщении
        notify_admin(user, f"Написал сообщение:\n_{message.text}_")

        # 3. Отвечаем пользователю
        response_text = (
            "✅ **Спасибо! Ваше сообщение получено.**\n\n"
            "Администратор уже получил ваше обращение и ответит вам в ближайшее время."
        )
        bot.reply_to(message, response_text, parse_mode="Markdown")

    except Exception as e:
        print(f"Ошибка в handle_text: {e}")


# --- ИСПРАВЛЕННЫЙ БЕСКОНЕЧНЫЙ ЦИКЛ ЗАПУСКА ---
if __name__ == '__main__':
    print("Бизнес ассистент запущен!")
    while True:
        try:
            bot.infinity_polling(skip_pending=True)
        except Exception as e:
            print(f"Сетевой сбой, перезапуск через 3 секунды... Ошибка: {e}")
            time.sleep(3)

