from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase


class UserCreateAPIViewTestCase(APITestCase):
    def setUp(self):
        self.data = {
            "username": "user1",
            "password": "12345678",
            "tg_chat_id": "123456789",
        }

    def test_create_user(self):
        """Тест на создание нового пользователя"""
        response = self.client.post("/auth/register/", self.data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = get_user_model().objects.get(username="user1")
        self.assertIsNotNone(user)
        self.assertEqual(user.username, "user1")
        self.assertTrue(user.check_password("12345678"))
        self.assertEqual(user.tg_chat_id, "123456789")

    def test_create_user_without_password(self):
        """Тест на создание пользователя без пароля"""
        data = {"username": "user2", "tg_chat_id": "12345678"}
        response = self.client.post("/auth/register/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
