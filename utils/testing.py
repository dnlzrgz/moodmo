import random
from django.contrib.auth import get_user_model
from django.utils import timezone
from moods.models import Activity, Mood

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


def create_fake_mood(user):
    mood = Mood.objects.create(
        user=user,
        mood=random.choice(Mood.MOOD_CHOICES)[0],
        note_title=fake.sentence(),
        date=timezone.now(),
        time=timezone.now(),
    )

    return mood


def create_fake_activity(user):
    activity = Activity.objects.create(
        user=user,
        name=fake.job()[:50],
    )
    return activity
