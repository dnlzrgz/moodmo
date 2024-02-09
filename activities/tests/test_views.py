from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from activities.models import Activity

USER_CREDENTIALS = {
    "username": "tester",
    "email": "test@test.com",
    "password": "test1234",
}


class ListViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(**USER_CREDENTIALS)
        self.url = reverse("activity_list")

    def test_authenticated_user(self):
        self.client.login(**USER_CREDENTIALS)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "activities/activity_list.html")

    def test_not_authenticated_user(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)


class CreateViewTest(TestCase):
    def setUp(self):
        self.url = reverse("activity_create")
        self.user = get_user_model().objects.create_user(**USER_CREDENTIALS)

    def test_authenticated_user(self):
        self.client.login(**USER_CREDENTIALS)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "activities/activity_create.html")

    def test_not_authenticated_user(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)


class UpdateViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(**USER_CREDENTIALS)
        self.activity = Activity.objects.create(user=self.user, name="Testing")
        self.url = reverse("activity_edit", args=[self.activity.id])

    def test_authenticated_user(self):
        self.client.login(**USER_CREDENTIALS)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "activities/activity_update.html")

    def test_authenticated_user_can_update_own_activity(self):
        self.client.login(**USER_CREDENTIALS)
        new_name = "Probing"
        response = self.client.post(self.url, {"name": new_name}, follow=True)

        self.assertEqual(response.status_code, 200)
        self.activity.refresh_from_db()
        self.assertEqual(self.activity.name, new_name)

    def test_authenticated_user_cannot_update_another_users_activity(self):
        other_user = get_user_model().objects.create_user(
            username="otheruser",
            email="other@test.com",
            password="other1234",
        )
        other_activity = Activity.objects.create(user=other_user, name="Other Activity")
        url = reverse("activity_edit", args=[other_activity.id])

        self.client.login(**USER_CREDENTIALS)
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)

    def test_not_authenticated_user(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)


class DeleteViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(**USER_CREDENTIALS)
        self.activity = Activity.objects.create(user=self.user, name="Testing")
        self.url = reverse("activity_delete", args=[self.activity.id])

    def test_authenticated_user(self):
        self.client.login(**USER_CREDENTIALS)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "activities/activity_delete.html")

    def test_authenticated_user_can_delete_own_activity(self):
        self.client.login(**USER_CREDENTIALS)
        response = self.client.post(self.url, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Activity.objects.filter(id=self.activity.id).exists())

    def test_authenticated_user_cannot_delete_another_user_activity(self):
        other_user = get_user_model().objects.create_user(
            username="otheruser",
            email="other@test.com",
            password="other1234",
        )
        other_activity = Activity.objects.create(
            user=other_user,
            name="Other Activity",
        )
        url = reverse("activity_delete", args=[other_activity.id])

        self.client.login(**USER_CREDENTIALS)
        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)

    def test_not_authenticated_user(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
