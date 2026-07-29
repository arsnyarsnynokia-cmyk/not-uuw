import os
import telebot
from telebot import types

TOKEN = os.environ.get('BOT_TOKEN')
ADMIN_ID = 7771113861

bot = telebot.TeleBot(TOKEN)


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


# 1. Обработка команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
  user = message.from_user
  notify_admin(user, "Запустил бота (/start)")

  markup = types.InlineKeyboardMarkup(row_width=1)
  btn_ref = types.InlineKeyboardButton(
      text="💳 Оформить бизнес-карту", url="https://vt.tiktok.com/ZS4eNAsBS/"
  )
  btn_contact = types.InlineKeyboardButton(
      text="💬 Связаться с нами", url="https://t.me/livernu_colbas"
  )
  btn_done = types.InlineKeyboardButton(
      text="✅ Карта оформлена", callback_data="card_done"
  )

  markup.add(btn_ref, btn_done, btn_contact)

  welcome_text = (
      f"Привет, {user.first_name}! 👋\n\n"
      "Я твой персональный **Бизнес-Ассистент**.\n"
      "Помогаю быстро оформить бизнес-карту на выгодных условиях "
      "и ответить на все интересующие вопросы.\n\n"
      "Выбери нужное действие ниже 👇"
  )

  bot.send_message(
      message.chat.id, welcome_text, reply_markup=markup, parse_mode="Markdown"
  )


# 2. Обработка кнопки «Карта оформлена»
@bot.callback_query_handler(func=lambda call: call.data == "card_done")
def handle_card_done(call):
  user = call.from_user
  notify_admin(user, "Нажал кнопку «Карта оформлена»")
  bot.answer_callback_query(call.id)

  response_text = (
      "Отлично! Ваша заявка принята на проверку банком (она занимает от 14 до"
      " 30 дней).\n\n"
      "Пожалуйста, пришлите в ответ на это сообщение ваш номер телефона, который"
      " вы указывали при оформлении, чтобы мы увидели вашу заявку."
  )
  bot.send_message(call.message.chat.id, response_text)


# 3. Обработка команды /help
@bot.message_handler(commands=['help'])
def send_help(message):
  notify_admin(message.from_user, "Запросил раздел помощи (/help)")
  help_text = (
      "❓ **Часто задаваемые вопросы (FAQ):**\n\n"
      "🔹 **Зачем нужна бизнес-карта?**\n"
      "Для удобного разделения личных средств и расходов бизнеса.\n\n"
      "🔹 **Сколько стоит обслуживание?**\n"
      "Бесплатное обслуживание и льготные тарифы при оформлении по"
      " ссылке.\n\n"
      "Если остались вопросы — напишите нам через «Связаться с нами»!"
  )
  bot.send_message(message.chat.id, help_text, parse_mode="Markdown")


# 4. Команда админа для ответа пользователю: /reply ID Текст
@bot.message_handler(commands=['reply'])
def reply_to_user(message):
  # Проверяем, что команду пишет именно админ
  if message.from_user.id != ADMIN_ID:
    return

  try:
    # Разбиваем команду на части: /reply, ID, сообщение
    parts = message.text.split(maxsplit=2)
    if len(parts) < 3:
      bot.reply_to(
          message,
          "⚠️ **Формат команды:**\n`/reply ID_пользователя Ваш текст`",
          parse_mode="Markdown",
      )
      return

    target_id = int(parts[1])
    text_to_send = parts[2]

    # Отправляем сообщение пользователю
    bot.send_message(
        target_id,
        f"💬 **Ответ от администратора:**\n\n{text_to_send}",
        parse_mode="Markdown",
    )
    bot.reply_to(message, "✅ **Сообщение успешно отправлено!**")

  except Exception as e:
    bot.reply_to(message, f"❌ Ошибка при отправке: `{e}`", parse_mode="Markdown")


# 5. Пересылка сообщений от пользователей админу
@bot.message_handler(content_types=['text'])
def handle_text(message):
  user = message.from_user

  if user.id != ADMIN_ID:
    notify_admin(user, f"Написал сообщение/номер: {message.text}")
    bot.reply_to(
        message,
        "Ваши данные приняты! Мы проверим заявку и свяжемся с вами.",
    )


if __name__ == '__main__':
  print("Бот успешно запущен и готов к работе...")
  bot.infinity_polling()
