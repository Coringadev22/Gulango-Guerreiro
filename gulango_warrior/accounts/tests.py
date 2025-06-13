from django.test import TestCase

from .models import CustomUser


class CustomUserModelTests(TestCase):
    """Tests for the :class:`CustomUser` model."""

    def test_default_not_instructor(self):
        user = CustomUser.objects.create_user(username="hero", password="123")
        self.assertFalse(user.is_instructor)

    def test_create_instructor(self):
        user = CustomUser.objects.create_user(
            username="mentor", password="123", is_instructor=True
        )
        self.assertTrue(user.is_instructor)
