import os
import random
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

logging.basicConfig(level=logging.INFO)

TOKEN = os.environ.get("BOT_TOKEN", "ВСТАВЬ_СВОЙ_ТОКЕН_СЮДА")

# Сообщения, которые бот будет отправлять
MESSAGES = [
    "Obtained Hope Fragment.",
    "Nagito's Report Card has been updated based on your experience with her.",
    "Hajime's Report Card has been updated based on your experience with him.",
    "Invite Hajime to hang out.",
    "Invite Nagito to hang out.",
    "You have obtained a present: Nagito's Undergarments.",
    "You have obtained a present: Hajime's Undergarments.",
    "Hajime and I grew a little closer today.",
    "Nagito and I grew a little closer today.",
]

# Счётчик сообщений на каждый чат
message_counters: dict[int, int] = {}
thresholds: dict[int, int] = {}

def get_new_threshold() -> int:
    """Случайный порог от 15 до 60."""
    return random.randint(15, 60)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.effective_chat:
        return

    chat_id = update.effective_chat.id

    # Инициализируем счётчик и порог для нового чата
    if chat_id not in message_counters:
        message_counters[chat_id] = 0
        thresholds[chat_id] = get_new_threshold()
        logging.info(f"Новый чат {chat_id}, первый порог: {thresholds[chat_id]}")

    message_counters[chat_id] += 1
    logging.info(f"Чат {chat_id}: сообщение {message_counters[chat_id]}/{thresholds[chat_id]}")

    if message_counters[chat_id] >= thresholds[chat_id]:
        text = random.choice(MESSAGES)
        await context.bot.send_message(chat_id=chat_id, text=text)
        logging.info(f"Чат {chat_id}: отправлено '{text}'")

        # Сбрасываем счётчик и устанавливаем новый порог
        message_counters[chat_id] = 0
        thresholds[chat_id] = get_new_threshold()
        logging.info(f"Чат {chat_id}: новый порог {thresholds[chat_id]}")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    logging.info("Бот запущен!")
    app.run_polling()

if __name__ == "__main__":
    main()
