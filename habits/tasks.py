# habits/tasks.py
from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import Habit
from .telegram_client import send_telegram_message_request
from django.utils.timezone import localtime


@shared_task
def check_due_habits():
    """
    Проверяет, какие привычки пора напомнить, и отправляет уведомления.
    """
    now_local = localtime(timezone.now())
    current_time = now_local.time().replace(second=0, microsecond=0)
    habits = Habit.objects.filter(time=current_time)

    for habit in habits:
        can_send = False
        if not habit.last_reminder_sent:
            can_send = True
        else:
            delta = now_local - habit.last_reminder_sent
            if delta >= timedelta(days=habit.repeat_days):
                can_send = True

        if not can_send:
            continue

        # Telegram chat_id
        chat_id = getattr(habit.owner, 'telegram_chat_id', None)
        if not chat_id:
            continue

        message = build_message_for_habit(habit)
        success = send_telegram_message_request(chat_id, message)

        if success:
            habit.last_reminder_sent = now_local
            habit.save(update_fields=['last_reminder_sent'])
            return 'message sent'


def build_message_for_habit(habit):
    text = f"<b>Напоминание о привычке</b>\n"
    text += f"Действие: <b>{habit.action}</b>\n"
    text += f"Место: <b>{habit.place}</b>\n"
    text += f"Время: {habit.time.strftime('%H:%M')}\n"
    if habit.is_pleasant:
        text += "Это приятная привычка!\n"
    else:
        if habit.reward:
            text += f"Вознаграждение: {habit.reward}\n"
        elif habit.related_habit:
            text += f"После этого выполните: {habit.related_habit.action}\n"
    text += f"Время выполнения: {habit.duration_seconds} сек."
    return text
