from celery import shared_task
from django.utils.timezone import now

from habits.models import Habit
from habits.services import send_telegram_message


@shared_task
def check_habits():
    """Проверяет привычки и отправляет сообщение, если подходит время их выполнения"""
    current_time = now().time()
    current_date = now().date()
    current_weekday = current_date.weekday() + 1

    current_hour = current_time.hour
    current_minute = current_time.minute

    daily_habits = Habit.objects.filter(
        periodicity_type=Habit.Periodicity.DAILY, is_pleasant=False
    )
    for habit in daily_habits:
        habit_hour = habit.time.hour
        habit_minute = habit.time.minute

        if habit_hour == current_hour and habit_minute == current_minute:
            message = f"Я буду {habit.action} в {habit.time.strftime('%H:%M')} в {habit.place}"
            if habit.user.tg_chat_id:
                send_telegram_message(message, habit.user.tg_chat_id)

    weekly_habits = Habit.objects.filter(
        periodicity_type=Habit.Periodicity.WEEKLY, is_pleasant=False
    )
    for habit in weekly_habits:
        habit_hour = habit.time.hour
        habit_minute = habit.time.minute

        if (
            current_weekday in (habit.weekdays or [])
            and habit_hour == current_hour
            and habit_minute == current_minute
        ):
            message = f"Я буду {habit.action} в {habit.time.strftime('%H:%M')} в {habit.place}"
            if habit.user.tg_chat_id:
                send_telegram_message(message, habit.user.tg_chat_id)
