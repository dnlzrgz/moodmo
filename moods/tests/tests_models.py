from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from moods.models import Mood


class MoodModelTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create(
            username="tester",
            email="test@test.com",
            password="tester1234",
        )

        self.mood = Mood.objects.create(
            user=self.user,
            mood=-2,
            note_title="Testing",
            note="Testing the mood model",
        )

    def test_mood_creation(self):
        self.assertEqual(self.mood.user, self.user)
        self.assertEqual(self.mood.mood, -2)
        self.assertEqual(self.mood.note_title, "Testing")
        self.assertEqual(self.mood.note, "Testing the mood model")

    def test_default_timestamp(self):
        mood = Mood.objects.create(user=self.user, mood=0)
        self.assertIsNotNone(mood.timestamp)
        self.assertEqual(mood.timestamp.date(), timezone.now().date())

    def test_last_modified_auto_now(self):
        old_last_modified = self.mood.last_modified
        self.mood.note = "Updated note"
        self.mood.save()

        self.assertNotEqual(self.mood.last_modified, old_last_modified)

    def test_valid_mood_choices(self):
        for choice, _ in Mood.MOOD_CHOICES:
            mood = Mood.objects.create(user=self.user, mood=choice)
            self.assertEqual(mood.mood, choice)

    def test_invalid_mood_choices(self):
        with self.assertRaises(ValidationError):
            mood_entry = Mood(user=self.user, mood=42)
            mood_entry.full_clean()

    def test_blank_note_title_and_note(self):
        mood = Mood.objects.create(user=self.user, mood=0)
        self.assertEqual(mood.note_title, "")
        self.assertEqual(mood.note, "")

    def test_delete_user_cascades_to_mood(self):
        user_id = self.user.id
        self.user.delete()

        with self.assertRaises(Mood.DoesNotExist):
            Mood.objects.get(user_id=user_id)

    def test_str_representation(self):
        expected_str = f"Mood added on {self.mood.timestamp}"
        self.assertEqual(str(self.mood), expected_str)
