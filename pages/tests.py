from django.test import TestCase
from django.urls import reverse


class HomePageTests(TestCase):
    def test_url_exists_at_correct_location(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):
        response = self.client.get(reverse("home"))
        self.assertTemplateUsed(response, "pages/home.html")


class RobotsTxtTests(TestCase):
    def test_url_exists_at_correct_location(self):
        response = self.client.get("/robots.txt")
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):
        response = self.client.get(reverse("robots"))
        self.assertEqual(response.status_code, 200)
        assert response["content-type"] == "text/plain"

    def test_template_name_correct(self):
        response = self.client.get(reverse("robots"))
        self.assertTemplateUsed(response, "pages/robots.txt")
