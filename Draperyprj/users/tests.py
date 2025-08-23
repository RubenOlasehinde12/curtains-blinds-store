# users/tests.py
from django.test import TestCase
from django.contrib.auth import get_user_model

class UserTests(TestCase):
    def test_create_user(self):
        u = get_user_model().objects.create_user(
            username="testuser",
            email="t@t.com",
            password="pass123"
        )
        self.assertEqual(u.username, "testuser")
        self.assertEqual(u.email, "t@t.com")
        self.assertTrue(u.check_password("pass123"))

    def test_create_superuser(self):
        s = get_user_model().objects.create_superuser(
            username="admin",
            email="a@a.com",
            password="adminpass"
        )
        self.assertTrue(s.is_staff)
        self.assertTrue(s.is_superuser)
