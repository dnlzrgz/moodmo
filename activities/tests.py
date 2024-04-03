from django.test import TestCase
from django.urls import reverse
from activities.models import Activity
from utils.testing import create_fake_user, create_fake_activity


class ListViewTest(TestCase):
    def setUp(self):
        self.credentials, self.user = create_fake_user()
        self.url = reverse("activity_list")

    def test_authenticated_user_can_access_view(self):
        self.client.login(**self.credentials)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "activities/activity_list.html")

    def test_not_authenticated_user_cannot_access_view(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)

    def test_authenticated_user_can_see_own_activities(self):
        self.client.login(**self.credentials)
        activity = create_fake_activity(self.user)

        response = self.client.get(self.url)

        self.assertContains(response, activity.name)

    def test_user_cannot_see_other_users_activities(self):
        activity = create_fake_activity(self.user)

        other_credentials, _ = create_fake_user()
        self.client.login(**other_credentials)

        response = self.client.get(self.url)

        self.assertNotContains(response, activity.name)


class CreateViewTest(TestCase):
    def setUp(self):
        self.credentials, self.user = create_fake_user()
        self.url = reverse("activity_create")

    def test_authenticated_user_can_access_view(self):
        self.client.login(**self.credentials)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "activities/activity_create.html")

    def test_not_authenticated_user_cannot_access_view(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)

    def test_authenticated_user_can_create_activity(self):
        self.client.login(**self.credentials)
        activity_data = {
            "name": "Testing",
        }

        response = self.client.post(self.url, data=activity_data)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Activity.objects.filter(name="Testing", user=self.user).exists()
        )

    def test_duplicated_activity_name_not_allowed(self):
        self.client.login(**self.credentials)
        activity = create_fake_activity(self.user)
        new_activity_data = {"name": activity.name}

        response = self.client.post(self.url, data=new_activity_data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response, "form", "name", "An activity with this name already exists."
        )


class UpdateViewTest(TestCase):
    def setUp(self):
        self.credentials, self.user = create_fake_user()
        self.activity = create_fake_activity(self.user)
        self.url = reverse("activity_edit", kwargs={"slug": self.activity.sqid})

    def test_authenticated_user_can_access_view(self):
        self.client.login(**self.credentials)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "activities/activity_update.html")

    def test_not_authenticated_user_cannot_access_view(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)

    def test_owner_can_update_activity(self):
        self.client.login(**self.credentials)
        new_activity_name = "Testing"
        update_data = {
            "name": new_activity_name,
        }

        response = self.client.post(self.url, data=update_data)

        self.assertEqual(response.status_code, 302)
        self.activity.refresh_from_db()
        self.assertEqual(self.activity.name, new_activity_name)

    def test_non_owner_cannot_update_activity(self):
        other_credentials, _ = create_fake_user()
        self.client.login(**other_credentials)
        new_activity_name = "Testing"
        update_data = {
            "name": new_activity_name,
        }

        response = self.client.post(self.url, data=update_data)

        self.assertEqual(response.status_code, 302)

    def test_activity_update_redirects_to_list_view(self):
        self.client.login(**self.credentials)
        new_activity_name = "Testing"
        update_data = {
            "name": new_activity_name,
        }

        response = self.client.post(
            self.url,
            data=update_data,
            follow=True,
        )
        self.assertRedirects(response, reverse("activity_list"))


class DeleteViewTest(TestCase):
    def setUp(self):
        self.credentials, self.user = create_fake_user()
        self.activity = create_fake_activity(self.user)
        self.url = reverse("activity_delete", kwargs={"slug": self.activity.sqid})

    def test_authenticated_user_can_access_view(self):
        self.client.login(**self.credentials)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "activities/activity_delete.html")

    def test_not_authenticated_user_cannot_access_view(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)

    def test_owner_can_delete_activity(self):
        self.client.login(**self.credentials)
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Activity.objects.filter(pk=self.activity.pk).exists())

    def test_non_owner_cannot_delete_activity(self):
        other_credentials, _ = create_fake_user()
        self.client.login(**other_credentials)
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 302)

    def test_activity_delete_redirects_to_list_view(self):
        self.client.login(**self.credentials)
        response = self.client.post(self.url, follow=True)

        self.assertRedirects(response, reverse("activity_list"))
