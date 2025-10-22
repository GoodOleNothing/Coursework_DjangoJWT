# habits/models.py
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from datetime import timedelta

User = settings.AUTH_USER_MODEL


class Habit(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="habits")
    action = models.CharField(max_length=200)  # ДЕЙСТВИЕ
    place = models.CharField(max_length=200)  # МЕСТО
    time = models.TimeField()  # ВРЕМЯ выполнения
    is_pleasant = models.BooleanField(default=False)  # признак приятной привычки
    related_habit = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.SET_NULL,
        related_name="linked_from"
    )  # связанная (приятная) привычка для полезной привычки
    reward = models.CharField(max_length=200, blank=True)  # вознаграждение (текст)
    duration_seconds = models.PositiveIntegerField(default=60)  # время на выполнение в секундах
    repeat_days = models.PositiveIntegerField(default=1,
        help_text="Повторность в днях (1..7), по умолчанию ежедневно")
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    # поле, чтобы отслеживать, когда в последний раз отправлялось напоминание
    last_reminder_sent = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['time', 'id']

    def clean(self):
        #  нельзя одновременно указать reward и related_habit
        if self.reward and self.related_habit:
            raise ValidationError("Нельзя указывать одновременно 'reward' и 'related_habit'.")

        #  время выполнения <= 120 сек
        if self.duration_seconds > 120:
            raise ValidationError("Время на выполнение не может быть больше 120 секунд.")

        #  связанные привычки могут быть только приятными
        if self.related_habit and not self.related_habit.is_pleasant:
            raise ValidationError("Связанная привычка должна быть помечена как приятная (is_pleasant=True).")

        #  приятная привычка не может иметь reward или related_habit
        if self.is_pleasant and (self.reward or self.related_habit):
            raise ValidationError("У приятной привычки не может быть ни 'reward', ни 'related_habit'.")

        #  repeat_days в диапазоне 1..7 (нельзя реже чем 1 раз в 7 дней)
        if self.repeat_days < 1 or self.repeat_days > 7:
            raise ValidationError("repeat_days должен быть от 1 до 7 (включительно).")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.owner} — {self.action} @ {self.time} ({'pleasant' if self.is_pleasant else 'useful'})"
