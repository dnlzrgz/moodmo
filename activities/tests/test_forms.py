from django.contrib.auth import get_user_model
from django.test import TestCase
from activities.forms import ActivityForm


class ActivityFormTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="tester",
            email="test@test.com",
            password="test1234",
        )

    def test_valid_form(self):
        data = {
            "name": "Testing",
        }
        form = ActivityForm(data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        data = {}
        form = ActivityForm(data)
        self.assertFalse(form.is_valid())

    def test_form_save(self):
        data = {"name": "Testing"}
        form = ActivityForm(data=data)
        self.assertTrue(form.is_valid())

        form.instance.user = self.user
        activity = form.save()

        self.assertEqual(activity.name, "Testing")
