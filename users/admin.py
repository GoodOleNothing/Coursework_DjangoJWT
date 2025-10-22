from django.contrib import admin
from users.models import User
from habits.models import Habit


@admin.register(User)
class Admin(admin.ModelAdmin):
    list_display = ('email', 'phone', 'avatar', 'city', 'telegram_chat_id','is_active')


@admin.register(Habit)
class Admin(admin.ModelAdmin):
    list_display = ('owner', 'action', 'place', 'time', 'is_pleasant', 'related_habit', 'reward', 'duration_seconds',
                    'repeat_days', 'duration_seconds', 'is_public', 'created_at', 'last_reminder_sent')
