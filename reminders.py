from apscheduler.schedulers.background import BackgroundScheduler
from google_sheets import get_unfinished_tasks
from config import SPREADSHEET_ID
from telegram import Bot

def send_reminders(bot_token):
    bot = Bot(bot_token)
    # Здесь ты можешь хранить список ID участников в Google Таблице
    user_ids = [12345678]  # заменить на список из таблицы
    for user_id in user_ids:
        unfinished = get_unfinished_tasks(SPREADSHEET_ID, user_id)
        if unfinished:
            bot.send_message(user_id, "Напоминание! У тебя есть невыполненные задания:\n" + "\n".join(unfinished))
        else:
            bot.send_message(user_id, "Все задания выполнены! Отлично 👏")

def start_scheduler(bot_token):
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_reminders, "cron", hour=9, args=[bot_token])
    scheduler.start()
