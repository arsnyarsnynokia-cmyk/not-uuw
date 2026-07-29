import os
import telebot
from telebot import types

# Считываем переменные из окружения облака
TOKEN = os.environ.get('BOT_TOKEN')
# ID администратора (считываем из переменных или ставим 0 по умолчанию)
ADMIN_ENV = os.environ.get('ADMIN_ID'7771113861)
ADMIN_ID = int(ADMIN_ENV) if ADMIN_ENV and ADMIN_ENV.isdigit() else 0

bot = telebot.TeleBot(TOKEN)


# Вспомогательная функция для отправки отчета админу
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

  # Создаем Inline-кнопки со ссылками
  markup = types.InlineKeyboardMarkup(row_width=1)

  btn_ref = types.InlineKeyboardButton(
      text="💳 Оформить бизнес-карту", url="https://vt.tiktok.com/ZS4eNAsBS/"
  )
  btn_contact = types.InlineKeyboardButton(
      text="💬 Связаться с нами", url="https://t.me/livernu_colbas"
  )

  markup.add(btn_ref, btn_contact)

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


# 2. Обработка команды /help
@bot.message_handler(commands=['help'])
def send_help(message):
  notify_admin(message.from_user, "Запросил раздел помощи (/help)")

  help_text = (
      "❓ **Часто задаваемые вопросы (FAQ):**\n\n"
      "🔹 **Зачем нужна бизнес-карта?**\n"
      "Для удобного разделения личных средств и расходов бизнеса, получения"
      " кэшбэка и спецпредложений от банков-партнеров.\n\n"
      "🔹 **Сколько стоит обслуживание?**\n"
      "При оформлении по нашей ссылке доступно полностью бесплатное обслуживание"
      " и льготные тарифы.\n\n"
      "🔹 **Кто может оформить?**\n"
      "Физические лица, самозанятые, ИП и руководители ООО.\n\n"
      "🔹 **Как быстро карта будет готова?**\n"
      "Реквизиты виртуальной карты выдаются моментально, а пластик доставит"
      " курьер за 1–2 дня.\n\n"
      "Если остались вопросы — напиши нам напрямую через кнопку «Связаться с"
      " нами»!"
  )

  bot.send_message(message.chat.id, help_text, parse_mode="Markdown")


# 3. Пересылка любых текстовых сообщений от пользователей
@bot.message_handler(content_types=['text'])
def handle_text(message):
  user = message.from_user

  # Отправляем уведомление админу (если пишет не сам админ)
  if user.id != ADMIN_ID:
    notify_admin(user, f"Написал сообщение: {message.text}")
    bot.reply_to(
        message,
        "Ваше сообщение получено! Чтобы оформить карту или написать нам,"
        " используйте меню в команде /start.",
    )


if __name__ == '__main__':
  print("Бот успешно запущен и готов к работе...")
  bot.infinity_polling()
