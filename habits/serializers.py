# habits/serializers.py
from rest_framework import serializers
from .models import Habit


class HabitSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Habit
        fields = [
            'id', 'owner', 'action', 'place', 'time', 'is_pleasant',
            'related_habit', 'reward', 'duration_seconds', 'repeat_days',
            'is_public', 'created_at'
        ]
        read_only_fields = ['id', 'owner', 'created_at']

    def validate(self, data):
        reward = data.get('reward', getattr(self.instance, 'reward', None))
        related = data.get('related_habit', getattr(self.instance, 'related_habit', None))
        is_pleasant = data.get('is_pleasant', getattr(self.instance, 'is_pleasant', False))
        duration = data.get('duration_seconds', getattr(self.instance, 'duration_seconds', 60))
        repeat_days = data.get('repeat_days', getattr(self.instance, 'repeat_days', 1))

        if reward and related:
            raise serializers.ValidationError("Нельзя указывать одновременно 'reward' и 'related_habit'.")

        if duration > 120:
            raise serializers.ValidationError("Время на выполнение не может быть больше 120 секунд.")

        if related and not related.is_pleasant:
            raise serializers.ValidationError("Связанная привычка должна быть помечена как приятная (is_pleasant=True).")

        if is_pleasant and (reward or related):
            raise serializers.ValidationError("У приятной привычки не может быть ни 'reward', ни 'related_habit'.")

        if repeat_days < 1 or repeat_days > 7:
            raise serializers.ValidationError("repeat_days должен быть от 1 до 7 (включительно).")

        return data
