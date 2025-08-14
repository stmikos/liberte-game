from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from config import BOT_TOKEN, SPREADSHEET_ID
from google_sheets import add_user, update_task_status, get_unfinished_tasks
from tasks import TASKS
from reminders import start_scheduler

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    add_user(SPREADSHEET_ID, user.id, user.username)
    await update.message.reply_text(
        "Добро пожаловать в Liberte 🌞\nВыбери в меню действие.",
        reply_markup=ReplyKeyboardMarkup(
            [["🗺 Задания", "📍 Карта"], ["📜 Правила", "🎁 Бонусы"], ["Не выполненные", "О проекте"]],
            resize_keyboard=True
        )
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.message.from_user.id

    if text == "🗺 Задания":
        await update.message.reply_text(TASKS[1] + "\nНапиши свой ответ.")
        context.user_data["current_task"] = 1

    elif text == "Не выполненные":
        unfinished = get_unfinished_tasks(SPREADSHEET_ID, user_id)
        if unfinished:
            await update.message.reply_text("\n".join(unfinished))
        else:
            await update.message.reply_text("Все задания выполнены!")

    elif "current_task" in context.user_data:
        task_number = context.user_data["current_task"]
        update_task_status(SPREADSHEET_ID, user_id, task_number, "выполнено", text)
        await update.message.reply_text(f"Задание {task_number} выполнено! ✅")
        context.user_data.pop("current_task")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

start_scheduler(BOT_TOKEN)
app.run_polling()
