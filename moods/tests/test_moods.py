import csv
import json
from io import BytesIO
from datetime import datetime
from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from moods.models import Mood
from utils.testing import create_fake_user, create_fake_mood


class MoodModelTest(TestCase):
    def setUp(self) -> None:
        self.credentials, self.user = create_fake_user()

    def test_mood_creation(self):
        mood = Mood.objects.create(
            user=self.user,
            mood=1,
            note_title="Testing",
            note="This is a test",
            date=timezone.now().date(),
            time=timezone.now().time(),
        )

        self.assertEqual(mood.user, self.user)
        self.assertEqual(mood.mood, 1)
        self.assertEqual(mood.note_title, "Testing")
        self.assertEqual(mood.note, "This is a test")
        self.assertIsNotNone(mood.date)
        self.assertIsNotNone(mood.time)
        self.assertIsNotNone(mood.last_modified)

    def test_get_absolute_url(self):
        mood = Mood.objects.create(
            user=self.user,
            mood=1,
            date=timezone.now().date(),
            time=timezone.now().time(),
        )

        expected_url = f"/moods/edit/{mood.sqid}"
        self.assertEqual(mood.get_absolute_url(), expected_url)

    def test_exception_if_required_fields_not_present(self):
        with self.assertRaises(IntegrityError):
            Mood.objects.create(user=self.user)


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


class ImportViewTest(TestCase):
    def setUp(self):
        self.credentials, self.user = create_fake_user()
        self.mood = create_fake_mood(self.user)
        self.url = reverse("import")

    def test_authenticated_user_can_access_view(self):
        self.client.login(**self.credentials)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "moods/import.html")

    def test_not_authenticated_user_cannot_access_view(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)

    def test_upload_csv_file(self):
        self.client.login(**self.credentials)

        csv_data = "mood,note_title,note,activities,date,time\n1,Test Mood 1,This is a test,Activity 1,2024-04-08,12:00:00"
        csv_file = BytesIO(csv_data.encode())
        csv_file.name = "test.csv"

        response = self.client.post(self.url, {"file": csv_file})

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Mood.objects.filter(user=self.user).exists())

    def test_upload_json_file(self):
        self.client.login(**self.credentials)

        json_data = [
            {
                "mood": 1,
                "note_title": "Testing",
                "note": "",
                "activities": ["Netflix"],
                "date": "2024-04-08",
                "time": "12:00:00",
            },
            {
                "mood": 2,
                "note_title": "Testing 2",
                "note": "This is a test.",
                "activities": ["Coding"],
                "date": "2024-04-08",
                "time": "13:00:00",
            },
        ]
        json_file = BytesIO(json.dumps(json_data).encode())
        json_file.name = "test.json"

        response = self.client.post(self.url, {"file": json_file})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Mood.objects.filter(user=self.user).exists())

    def test_upload_unsupported_file_type(self):
        self.client.login(**self.credentials)

        text_file = BytesIO(b"\n")
        text_file.name = "test.txt"
        response = self.client.post(self.url, {"file": text_file})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Only CSV or JSON files are supported.")

    def test_upload_file_exceeding_size(self):
        self.client.login(**self.credentials)
        large_file = BytesIO(b"Large file data" * 1_000_000)
        large_file.name = "large_file.csv"

        response = self.client.post(self.url, {"file": large_file})

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "The file is too big. The maximum support filesize is 2.5 MB.",
        )


class ExportViewTest(TestCase):
    def setUp(self):
        self.credentials, self.user = create_fake_user()
        self.url = reverse("export")

    def test_authenticated_user_can_access_view(self):
        self.client.login(**self.credentials)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "moods/export.html")

    def test_not_authenticated_user_cannot_access_view(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)

    def test_export_json_file(self):
        self.client.login(**self.credentials)
        current_date = datetime.now().strftime("%Y_%m_%d")
        moods = [create_fake_mood(self.user) for _ in range(5)]

        response = self.client.post(self.url, {"export_format": "json"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get("Content-Disposition"),
            f'attachment; filename="moodmo_export_{current_date}.json"',
        )
        self.assertEqual(response["Content-Type"], "application/json")

        exported_data = json.loads(response.content)
        self.assertEqual(len(exported_data), len(moods))

    def test_export_csv_file(self):
        self.client.login(**self.credentials)
        current_date = datetime.now().strftime("%Y_%m_%d")
        moods = [create_fake_mood(self.user) for _ in range(5)]

        response = self.client.post(self.url, {"export_format": "csv"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get("Content-Disposition"),
            f'attachment; filename="moodmo_export_{current_date}.csv"',
        )
        self.assertEqual(response["Content-Type"], "text/csv")

        exported_data = response.content.decode("utf-8")
        csv_reader = csv.reader(exported_data.splitlines())
        self.assertEqual(len(list(csv_reader)) - 1, len(moods))
