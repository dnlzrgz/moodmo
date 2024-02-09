from django.contrib.auth import get_user_model
from django.test import TestCase

from activities.models import Activity


class ActivityModelTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create(
            username="tester",
            email="test@test.com",
            password="tester1234",
        )

        self.activity = Activity.objects.create(
            user=self.user,
            name="Testing",
        )

    def test_activity_creation(self):
        self.assertEqual(self.activity.user, self.user)
        self.assertEqual(self.activity.name, "Testing")

    def test_delete_user_cascades_to_activities(self):
        user_id = self.user.id
        self.user.delete()

        with self.assertRaises(Activity.DoesNotExist):
            Activity.objects.get(user_id=user_id)

    def test_get_absolute_url(self):
        expected_url = f"/activities/edit/{self.activity.pk}"
        self.assertEqual(self.activity.get_absolute_url(), expected_url)

    def test_str_representation(self):
        self.assertEqual(str(self.activity), "Testing")
