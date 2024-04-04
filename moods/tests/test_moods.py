from django.test import TestCase
from django.urls import reverse
from moods.models import Mood
from utils.testing import create_fake_user, create_fake_mood


class ListViewTest(TestCase):
    def setUp(self):
        self.credentials, self.user = create_fake_user()
        self.url = reverse("mood_list")

    def test_authenticated_user_can_access_view(self):
        self.client.login(**self.credentials)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "moods/mood_list.html")

    def test_not_authenticated_user_cannot_access_view(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)

    def test_authenticated_user_can_see_own_moods(self):
        self.client.login(**self.credentials)
        mood = create_fake_mood(self.user)

        response = self.client.get(self.url)

        self.assertContains(response, mood.note_title)

    def test_user_cannot_see_other_users_moods(self):
        mood = create_fake_mood(self.user)

        other_credentials, _ = create_fake_user()
        self.client.login(**other_credentials)

        response = self.client.get(self.url)

        self.assertNotContains(response, mood.note_title)


class CreateViewTest(TestCase):
    def setUp(self):
        self.credentials, self.user = create_fake_user()
        self.url = reverse("mood_create")

    def test_authenticated_user_can_access_view(self):
        self.client.login(**self.credentials)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "moods/mood_create.html")

    def test_not_authenticated_user_cannot_access_view(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)

    def test_authenticated_user_can_create_mood(self):
        self.client.login(**self.credentials)
        mood_data = {
            "mood": 1,
            "date": "2024-04-04",
            "time": "12:00:00",
        }

        response = self.client.post(self.url, data=mood_data)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Mood.objects.filter(mood=1, user=self.user).exists())


class UpdateViewTest(TestCase):
    def setUp(self):
        self.credentials, self.user = create_fake_user()
        self.mood = create_fake_mood(self.user)
        self.url = reverse("mood_edit", kwargs={"slug": self.mood.sqid})

    def test_authenticated_user_can_access_view(self):
        self.client.login(**self.credentials)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "moods/mood_update.html")

    def test_not_authenticated_user_cannot_access_view(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)

    def test_owner_can_update_mood(self):
        self.client.login(**self.credentials)
        new_note = "Testing"
        update_data = {
            "mood": 1,
            "note": new_note,
            "date": "2024-04-04",
            "time": "12:00:00",
        }

        response = self.client.post(self.url, data=update_data)

        self.assertEqual(response.status_code, 302)
        self.mood.refresh_from_db()
        self.assertEqual(self.mood.note, new_note)

    def test_non_owner_cannot_update_mood(self):
        other_credentials, _ = create_fake_user()
        self.client.login(**other_credentials)
        new_note = "Testing"
        update_data = {
            "mood": 1,
            "note": new_note,
            "date": "2024-04-04",
            "time": "12:00:00",
        }

        response = self.client.post(self.url, data=update_data)

        self.assertEqual(response.status_code, 302)

    def test_mood_update_redirects_to_list_view(self):
        self.client.login(**self.credentials)
        new_note = "Testing"
        update_data = {
            "mood": 1,
            "note": new_note,
            "date": "2024-04-04",
            "time": "12:00:00",
        }

        response = self.client.post(self.url, data=update_data, follow=True)

        self.assertRedirects(response, reverse("mood_list"))


class DeleteViewTest(TestCase):
    def setUp(self):
        self.credentials, self.user = create_fake_user()
        self.mood = create_fake_mood(self.user)
        self.url = reverse("mood_delete", kwargs={"slug": self.mood.sqid})

    def test_authenticated_user_can_access_view(self):
        self.client.login(**self.credentials)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "moods/mood_delete.html")

    def test_not_authenticated_user_cannot_access_view(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)

    def test_owner_can_delete_mood(self):
        self.client.login(**self.credentials)
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Mood.objects.filter(pk=self.mood.pk).exists())

    def test_non_owner_cannot_delete_mood(self):
        other_credentials, _ = create_fake_user()
        self.client.login(**other_credentials)
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 302)

    def test_mood_delete_redirects_to_list_view(self):
        self.client.login(**self.credentials)
        response = self.client.post(self.url, follow=True)

        self.assertRedirects(response, reverse("mood_list"))
