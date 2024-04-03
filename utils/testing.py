from django.contrib.auth import get_user_model
from activities.models import Activity

try:
    from faker import Faker

    fake = Faker()
except ImportError:
    raise ImportError(
        "Faker package is required. Maybe you're in the wrong environment."
    )


def create_fake_user():
    credentials = {
        "username": fake.name(),
        "email": fake.email(),
        "password": fake.password(),
    }
    user = get_user_model().objects.create_user(**credentials)

    return (credentials, user)


def create_fake_activity(user):
    activity = Activity.objects.create(
        user=user,
        name=fake.job()[:50],
    )
    return activity
