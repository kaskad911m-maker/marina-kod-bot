"""
Бот @marina_kod_bot — только мини-приложение скрининга (Web App).
Без Гуру/Арви и без Groq. Токен в TELEGRAM_TOKEN — только этого бота.
"""
import logging
import os
import sys

from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
MINI_APP_URL = os.getenv(
    "MINI_APP_URL",
    "https://screening-web-seven.vercel.app/mini-app.html",
).strip()


async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return
    logger.info("marina_kod_bot /start user=%s", update.effective_user.id if update.effective_user else None)

    text = (
        "Привет! ✨\n\n"
        "Нажми «Открыть приложение» — откроется мини-приложение: расчёт по дате рождения и запись на скрининг.\n\n"
        "Кнопка «Мой код» внизу слева тоже ведёт туда. Вторая кнопка — открыть в браузере."
    )
    markup = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("✨ Открыть приложение", web_app=WebAppInfo(url=MINI_APP_URL))],
            [InlineKeyboardButton("Открыть в браузере", url=MINI_APP_URL)],
        ]
    )
    try:
        await update.message.reply_text(text, reply_markup=markup)
    except Exception as e:
        logger.exception("cmd_start failed: %s", e)
        await update.message.reply_text(f"{text}\n\nСсылка: {MINI_APP_URL}")


def main():
    if not TELEGRAM_TOKEN or not TELEGRAM_TOKEN.strip():
        logging.error(
            "Нет TELEGRAM_TOKEN. Railway → сервис worker → Variables → "
            "добавь TELEGRAM_TOKEN = токен @marina_kod_bot из BotFather"
        )
        sys.exit(1)
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", cmd_start))
    logger.info("marina-kod-bot запущен, MINI_APP_URL=%s", MINI_APP_URL)
    app.run_polling()


if __name__ == "__main__":
    main()
