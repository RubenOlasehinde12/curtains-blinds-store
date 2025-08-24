# pages/tests.py
from django.test import SimpleTestCase  
from django.urls import reverse, resolve

class HomepageTests(SimpleTestCase):
    def test_home_url_name_resolves(self):
        match = resolve(reverse("home"))
        self.assertEqual(match.view_name, "home")

    def test_home_status_code_200(self):
        resp = self.client.get(reverse("home"))
        self.assertEqual(resp.status_code, 200)

    def test_home_uses_template(self):
        resp = self.client.get(reverse("home"))
        self.assertTemplateUsed(resp, "home.html")
