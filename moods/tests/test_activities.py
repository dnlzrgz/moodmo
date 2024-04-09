from django.test import TestCase
from django.urls import reverse
from moods.forms import ActivityForm
from moods.models import Activity
from utils.testing import create_fake_user, create_fake_activity


class ActivityModelTest(TestCase):
    def setUp(self) -> None:
        self.credentials, self.user = create_fake_user()

    def test_activity_creation(self):
        activity = Activity.objects.create(
            user=self.user,
            name="Testing",
        )

        self.assertEqual(activity.user, self.user)
        self.assertEqual(activity.name, "Testing")

    def test_get_absolute_url(self):
        activity = Activity.objects.create(
            user=self.user,
            name="Testing",
        )

        expected_url = f"/moods/activities/edit/{activity.sqid}"
        self.assertEqual(activity.get_absolute_url(), expected_url)


class ActivityFormTest(TestCase):
    def test_activity_form_valid(self):
        data = {"name": "testing"}
        form = ActivityForm(data=data)
        self.assertTrue(form.is_valid())

    def test_activity_form_invalid_name(self):
        data = {"name": ""}
        form = ActivityForm(data=data)
        self.assertFalse(form.is_valid())


class ListViewTest(TestCase):
    def setUp(self):
        self.credentials, self.user = create_fake_user()
        self.url = reverse("activity_list")

    def test_authenticated_user_can_access_view(self):
        self.client.login(**self.credentials)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "moods/activity_list.html")

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
        self.assertTemplateUsed(response, "moods/activity_create.html")

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

    def test_activity_with_duplicated_name_do_nothing(self):
        self.client.login(**self.credentials)
        activity = create_fake_activity(self.user)
        new_activity_data = {"name": activity.name}

        response = self.client.post(self.url, data=new_activity_data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Activity.objects.filter(user=self.user).count(), 1)


class UpdateViewTest(TestCase):
    def setUp(self):
        self.credentials, self.user = create_fake_user()
        self.activity = create_fake_activity(self.user)
        self.url = reverse("activity_edit", kwargs={"slug": self.activity.sqid})

    def test_authenticated_user_can_access_view(self):
        self.client.login(**self.credentials)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "moods/activity_update.html")

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
        self.assertTemplateUsed(response, "moods/activity_delete.html")

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
