from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from habits.models import Habit


class HabitViewSetTestCase(APITestCase):
    def setUp(self):
        self.user1 = get_user_model().objects.create_user(
            username="user1", password="12345678"
        )
        self.user2 = get_user_model().objects.create_user(
            username="user2", password="12345678"
        )
        self.client = APIClient()

        self.habit_data = {
            "place": "Парк",
            "time": "07:30:00",
            "action": "Бегать",
            "is_pleasant": False,
            "duration": 60,
            "is_public": True,
            "periodicity_type": "DAILY",
            "weekdays": None,
            "reward": "Выпить воды",
            "related_habit": None,
        }

        Habit.objects.all().delete()

    def test_create_habit_for_user1(self):
        """Тест на создание привычки для пользователя user1"""
        self.client.force_authenticate(user=self.user1)
        response = self.client.post("/habits/", self.habit_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 1)
        self.assertEqual(Habit.objects.first().user, self.user1)

    def test_read_habit_for_user1(self):
        """Тест на получение привычки для пользователя user1"""
        self.client.force_authenticate(user=self.user1)
        self.client.post("/habits/", self.habit_data, format="json")

        habit = Habit.objects.first()
        response = self.client.get(f"/habits/{habit.id}/", format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["user"], self.user1.id)

    def test_update_habit_for_user1(self):
        """Тест на обновление привычки для пользователя user1"""
        self.client.force_authenticate(user=self.user1)
        self.client.post("/habits/", self.habit_data, format="json")

        habit = Habit.objects.first()
        updated_data = {
            "place": "Лес",
            "time": "08:00:00",
            "action": "Прогулка",
            "is_pleasant": False,
            "duration": 120,
            "is_public": True,
            "periodicity_type": "DAILY",
            "weekdays": None,
            "reward": "Термос с чаем",
            "related_habit": None,
        }
        response = self.client.put(f"/habits/{habit.id}/", updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        habit.refresh_from_db()
        self.assertEqual(habit.place, "Лес")
        self.assertEqual(habit.action, "Прогулка")
        self.assertEqual(habit.reward, "Термос с чаем")

    def test_delete_habit_for_user1(self):
        """Тест на удаление привычки для пользователя user1"""
        self.client.force_authenticate(user=self.user1)
        self.client.post("/habits/", self.habit_data, format="json")

        habit = Habit.objects.first()
        response = self.client.delete(f"/habits/{habit.id}/", format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.count(), 0)

    def test_user2_cannot_access_user1_data(self):
        """Тест, что user2 не может получить доступ к данным user1"""
        self.client.force_authenticate(user=self.user1)
        self.client.post("/habits/", self.habit_data, format="json")

        self.client.force_authenticate(user=self.user2)
        habit = Habit.objects.first()
        response = self.client.get(f"/habits/{habit.id}/", format="json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = self.client.get("/habits/", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 0)


class HabitValidationTestCase(APITestCase):
    def setUp(self):
        self.user1 = get_user_model().objects.create_user(
            username="user1", password="12345678"
        )
        self.client = APIClient()

        self.related_habit = Habit.objects.create(
            user=self.user1,
            place="Дом",
            time="08:00:00",
            action="Читать",
            is_pleasant=True,
            duration=60,
            is_public=True,
            periodicity_type="DAILY",
            reward=None,
            related_habit=None,
        )

        self.incorrect_data1 = {
            "place": "Парк",
            "time": "07:30:00",
            "action": "Бегать",
            "is_pleasant": False,
            "duration": 60,
            "is_public": True,
            "periodicity_type": "DAILY",
            "weekdays": None,
            "reward": "Выпить воды",
            "related_habit": self.related_habit.id,
        }

        self.incorrect_data2 = {
            "place": "Парк",
            "time": "07:30:00",
            "action": "Бегать",
            "is_pleasant": False,
            "duration": 125,
            "is_public": True,
            "periodicity_type": "DAILY",
            "weekdays": None,
            "reward": "Выпить воды",
            "related_habit": None,
        }

        self.incorrect_data3 = {
            "place": "Парк",
            "time": "07:30:00",
            "action": "Бегать",
            "is_pleasant": False,
            "duration": 60,
            "is_public": True,
            "periodicity_type": "WEEKLY",
            "weekdays": [],
            "reward": "Выпить воды",
            "related_habit": None,
        }

        self.incorrect_data4 = {
            "place": "Парк",
            "time": "07:30:00",
            "action": "Бегать",
            "is_pleasant": False,
            "duration": 60,
            "is_public": True,
            "periodicity_type": "DAILY",
            "weekdays": [1],
            "reward": "Выпить воды",
            "related_habit": None,
        }

    def test_create_habit_with_reward_and_related_habit(self):
        """Тест на ошибку при указании одновременно вознаграждения и связанной привычки"""
        self.client.force_authenticate(user=self.user1)
        response = self.client.post("/habits/", self.incorrect_data1, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "Нельзя указать одновременно и вознаграждение, и связанную привычку",
            str(response.data),
        )

    def test_create_habit_with_duration_more_than_120(self):
        """Тест на ошибку при времени выполнения больше 120 секунд"""
        self.client.force_authenticate(user=self.user1)
        response = self.client.post("/habits/", self.incorrect_data2, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "Время выполнения не может превышать 120 секунд", str(response.data)
        )

    def test_create_habit_with_no_weekdays_for_weekly(self):
        """Тест на ошибку при отсутствии дней недели для недельной привычки"""
        self.client.force_authenticate(user=self.user1)
        response = self.client.post("/habits/", self.incorrect_data3, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "Привычка должна выполняться хотя бы раз в 7 дней. Укажите дни недели",
            str(response.data),
        )

    def test_create_habit_with_weekdays_for_daily(self):
        """Тест на ошибку при указании дней недели для ежедневной привычки"""
        self.client.force_authenticate(user=self.user1)
        response = self.client.post("/habits/", self.incorrect_data4, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class PublicHabitListAPIViewTest(APITestCase):
    def setUp(self):
        self.user1 = get_user_model().objects.create_user(
            username="user1", password="12345678"
        )
        self.client = APIClient()

        self.public_habit = Habit.objects.create(
            user=self.user1,
            place="Парк",
            time="07:00:00",
            action="Бег",
            is_pleasant=True,
            duration=30,
            is_public=True,
            periodicity_type="DAILY",
        )

        self.private_habit = Habit.objects.create(
            user=self.user1,
            place="Дом",
            time="20:00:00",
            action="Чтение",
            is_pleasant=False,
            duration=15,
            is_public=False,
            periodicity_type="DAILY",
        )

    def test_public_habit_list(self):
        """Тест на список публичных привычек"""
        self.client.force_authenticate(user=self.user1)
        response = self.client.get("/habits/public/", format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
