from django.contrib import admin
from users.models import User


@admin.register(User)
class Admin(admin.ModelAdmin):
    list_display = ('email', 'phone', 'avatar', 'city', 'is_active')