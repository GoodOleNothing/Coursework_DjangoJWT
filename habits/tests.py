from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.utils import timezone
from django.contrib.auth import get_user_model
from habits.models import Habit
from habits.serializers import HabitSerializer

User = get_user_model()


class UsersAPITest(TestCase):
    """
    Тестирование API пользователей (регистрация, Telegram chat_id).
    """
    def setUp(self):
        self.client = APIClient()
        self.register_url = "/api/users/register/"
        self.telegram_url = "/api/users/set_telegram_chat/"

    def test_user_registration(self):
        data = {
            "email": "test@example.com",
            "password": "testpassword123"
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email="test@example.com").exists())

    def test_set_telegram_chat_id_authenticated(self):
        user = User.objects.create_user(email="user@example.com", password="12345")
        self.client.force_authenticate(user=user)
        response = self.client.post(self.telegram_url, {"telegram_chat_id": "999888777"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user.refresh_from_db()
        self.assertEqual(user.telegram_chat_id, "999888777")

    def test_set_telegram_chat_id_unauthenticated(self):
        response = self.client.post(self.telegram_url, {"telegram_chat_id": "123"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class HabitsAPITest(TestCase):
    """
    Тестирование CRUD привычек и публичного списка.
    """
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email="habituser@example.com", password="12345")
        self.client.force_authenticate(user=self.user)
        self.habits_url = "/api/habits/"
        self.public_url = "/api/habits/public/"

    def test_create_habit(self):
        data = {
            "action": "Прогулка после обеда",
            "place": "Парк",
            "time": timezone.now().time().strftime("%H:%M:%S"),
            "is_pleasant": False,
            "duration_seconds": 60,
            "repeat_days": 1,
            "is_public": False
        }
        response = self.client.post(self.habits_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Habit.objects.filter(owner=self.user, action="Прогулка после обеда").exists())

    def test_validation_reward_and_related_conflict(self):
        pleasant = Habit.objects.create(
            owner=self.user,
            action="Послушать музыку",
            is_pleasant=True,
            time=timezone.now().time(),
            place="Дом"
        )
        data = {
            "action": "Учить английский",
            "place": "Дом",
            "time": timezone.now().time().strftime("%H:%M:%S"),
            "is_pleasant": False,
            "reward": "Шоколадка",
            "related_habit": pleasant.id,
            "duration_seconds": 60,
            "repeat_days": 1
        }
        response = self.client.post(self.habits_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("reward", str(response.data))

    def test_public_habits_list(self):
        Habit.objects.create(
            owner=self.user,
            action="Полезная привычка",
            is_public=True,
            time=timezone.now().time(),
            place="Дом"
        )
        response = self.client.get(self.public_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data["results"]) >= 1)

    def test_user_sees_only_own_habits(self):
        other = User.objects.create_user(email="other@example.com", password="123")
        Habit.objects.create(
            owner=other,
            action="Чужая привычка",
            time=timezone.now().time(),
            place="Офис"
        )
        Habit.objects.create(
            owner=self.user,
            action="Моя привычка",
            time=timezone.now().time(),
            place="Дом"
        )

        response = self.client.get(self.habits_url)
        actions = [item["action"] for item in response.data["results"]]
        self.assertIn("Моя привычка", actions)
        self.assertNotIn("Чужая привычка", actions)


class HabitSerializerTest(TestCase):
    """
    Отдельно проверяем сериализатор HabitSerializer.
    """
    def setUp(self):
        self.user = User.objects.create_user(email="serial@example.com", password="123")

    def test_pleasant_habit_cannot_have_reward(self):
        data = {
            "action": "Слушать музыку",
            "is_pleasant": True,
            "reward": "Конфета",
            "duration_seconds": 60,
            "repeat_days": 1,
            "time": timezone.now().time(),
            "place": "Дом"
        }
        serializer = HabitSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_repeat_days_must_be_in_range(self):
        data = {
            "action": "Тренировка",
            "is_pleasant": False,
            "duration_seconds": 60,
            "repeat_days": 10,  # Ошибка
            "time": timezone.now().time(),
            "place": "Дом"
        }
        serializer = HabitSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("repeat_days", str(serializer.errors))
