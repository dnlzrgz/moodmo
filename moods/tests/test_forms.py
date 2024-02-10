from datetime import datetime
from django.contrib.auth import get_user_model
from django.test import TestCase
from moods.forms import MoodForm


class MoodFormTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="tester",
            email="test@test.com",
            password="test1234",
        )

    def test_valid_form(self):
        data = {
            "mood": 1,
            "timestamp": datetime.utcnow(),
        }
        form = MoodForm(user=self.user, data=data)

        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        data = {
            "timestamp": datetime.utcnow(),
        }
        form = MoodForm(user=self.user, data=data)

        self.assertFalse(form.is_valid())

    def test_form_save(self):
        data = {
            "mood": 1,
            "note_title": "Testing",
            "note": "Test",
            "timestamp": datetime.utcnow(),
        }
        form = MoodForm(user=self.user, data=data)
        self.assertTrue(form.is_valid())

        form.instance.user = self.user
        mood = form.save()

        self.assertEqual(mood.mood, 1)
        self.assertEqual(mood.note_title, "Testing")
        self.assertEqual(mood.note, "Test")
