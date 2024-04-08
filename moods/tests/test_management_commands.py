from django.test import TestCase
from django.core.management import call_command
from moods.models import Activity, Mood
from utils.testing import create_fake_activity, create_fake_user, create_fake_mood


class AddActivitiesCommandTest(TestCase):
    def setUp(self):
        self.credentials, self.user = create_fake_user()

    def test_command(self):
        call_command("add_activities", number=10)

        self.assertEqual(Activity.objects.filter(user=self.user).count(), 10)


class DeleteActivitiesCommandTest(TestCase):
    def setUp(self):
        self.credentials, self.user = create_fake_user()
        self.activities = [create_fake_activity(self.user) for _ in range(5)]

    def test_command(self):
        self.assertEqual(
            Activity.objects.filter(user=self.user).count(), len(self.activities)
        )

        call_command("delete_activities")

        self.assertEqual(Activity.objects.filter(user=self.user).count(), 0)


class AddMoodsCommandTest(TestCase):
    def setUp(self):
        self.credentials, self.user = create_fake_user()

    def test_command(self):
        call_command("add_moods", number=10)

        self.assertEqual(Mood.objects.filter(user=self.user).count(), 10)


class DeleteMoodsCommandTest(TestCase):
    def setUp(self):
        self.credentials, self.user = create_fake_user()
        self.moods = [create_fake_mood(self.user) for _ in range(5)]

    def test_command(self):
        self.assertEqual(Mood.objects.filter(user=self.user).count(), len(self.moods))

        call_command("delete_moods")

        self.assertEqual(Mood.objects.filter(user=self.user).count(), 0)
