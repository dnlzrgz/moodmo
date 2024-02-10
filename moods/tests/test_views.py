from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from datetime import datetime

from moods.models import Mood

USER_CREDENTIALS = {
    "username": "tester",
    "email": "test@test.com",
    "password": "test1234",
}


class ListViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(**USER_CREDENTIALS)
        self.url = reverse("mood_list")

    def test_authenticated_user_without_htmx_header(self):
        self.client.login(**USER_CREDENTIALS)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "moods/mood_list.html")

    def test_authenticated_user_with_htmx_header(self):
        self.client.login(**USER_CREDENTIALS)
        response = self.client.get(self.url, headers={"HX-Request": "True"})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "moods/hx_mood_list.html")

    def test_not_authenticated_user(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)


class SearchViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(**USER_CREDENTIALS)
        self.url = reverse("mood_search")

    def test_authenticated_user(self):
        self.client.login(**USER_CREDENTIALS)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "moods/mood_search.html")

    def test_not_authenticated_user(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)


class SearchResultsViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(**USER_CREDENTIALS)
        self.url = reverse("mood_search_results")

    def test_authenticated_user_without_correct_header(self):
        self.client.login(**USER_CREDENTIALS)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)

    def test_authenticated_user_with_correct_header(self):
        self.client.login(**USER_CREDENTIALS)
        response = self.client.get(self.url, headers={"HX-Request": "True"})

        self.assertEqual(response.status_code, 200)

    def test_not_authenticated_user(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)


class CreateViewTest(TestCase):
    def setUp(self):
        self.url = reverse("mood_create")
        self.user = get_user_model().objects.create_user(**USER_CREDENTIALS)

    def test_authenticated_user(self):
        self.client.login(**USER_CREDENTIALS)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "moods/mood_create.html")

    def test_not_authenticated_user(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)

    def test_authenticated_user_can_create_mood(self):
        self.client.login(**USER_CREDENTIALS)
        data = {
            "mood": 1,
            "note_title": "Testing",
            "note": "Testing",
            "timestamp": datetime.utcnow(),
        }

        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)

        self.assertEqual(Mood.objects.count(), 1)

        mood = Mood.objects.first()
        self.assertEqual(mood.user, self.user)
        self.assertEqual(mood.mood, 1)
        self.assertEqual(mood.note_title, "Testing")
        self.assertEqual(mood.note, "Testing")
        self.assertIsNotNone(mood.timestamp)


class UpdateViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(**USER_CREDENTIALS)
        self.mood = Mood.objects.create(user=self.user, mood=1, note="Test")
        self.url = reverse("mood_edit", args=[self.mood.id])

    def test_authenticated_user(self):
        self.client.login(**USER_CREDENTIALS)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "moods/mood_update.html")

    def test_authenticated_user_can_update_mood_entry(self):
        self.client.login(**USER_CREDENTIALS)
        self.mood.note_title = "Testing"

        post_data = self.mood.__dict__.copy()
        post_data.pop("search_vector", None)

        response = self.client.post(self.url, post_data)
        self.assertEqual(response.status_code, 302)

        updated_mood = Mood.objects.get(id=self.mood.id)
        self.assertEqual(updated_mood.note_title, "Testing")
        self.assertEqual(updated_mood.note, "Test")

    def test_authenticated_user_cannot_update_another_users_mood_entry(self):
        get_user_model().objects.create_user(
            username="anotheruser",
            email="another@example.com",
            password="another1234",
        )

        self.client.login(username="anotheruser", password="another1234")
        updated_mood = {
            "mood": -2,
        }
        response = self.client.post(self.url, data=updated_mood)

        self.assertRedirects(response, reverse("mood_list"))

        updated_mood = Mood.objects.get(id=self.mood.id)
        self.assertNotEqual(updated_mood.mood, -2)

    def test_not_authenticated_user(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)


class DeleteViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(**USER_CREDENTIALS)
        self.mood = Mood.objects.create(user=self.user, mood=1)
        self.url = reverse("mood_delete", args=[self.mood.id])

    def test_authenticated_user(self):
        self.client.login(**USER_CREDENTIALS)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "moods/mood_delete.html")

    def test_authenticated_user_can_delete_mood_entry(self):
        self.client.login(**USER_CREDENTIALS)
        response = self.client.post(self.url, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Mood.objects.filter(id=self.mood.id).exists())

    def test_authenticated_user_cannot_delete_another_users_mood_entry(self):
        get_user_model().objects.create_user(
            username="another",
            email="another@another.com",
            password="another1234",
        )

        self.client.login(username="another", password="another1234")
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse("mood_list"))

    def test_not_authenticated_user(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)


class ExportViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(**USER_CREDENTIALS)
        self.url = reverse("mood_export")

    def test_authenticated_user(self):
        self.client.login(**USER_CREDENTIALS)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "moods/mood_export.html")

    def test_not_authenticated_user(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)


class ImportViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(**USER_CREDENTIALS)
        self.url = reverse("mood_import")

    def test_authenticated_user(self):
        self.client.login(**USER_CREDENTIALS)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "moods/mood_import.html")

    def test_not_authenticated_user(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)
