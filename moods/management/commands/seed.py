import random
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from moods.models import Activity, Mood
from moods.management.commands.add_activities import DUMMY_ACTIVITIES

try:
    from faker import Faker

    fake = Faker()
except ImportError:
    raise ImportError(
        "Faker package is required for this command. Maybe you're in the wrong environment."
    )


class Command(BaseCommand):
    help = "Seed database with users, activities, and moods."

    def add_arguments(self, parser):
        parser.add_argument(
            "--users",
            type=int,
            help="Number of users to add",
            default=20,
        )
        parser.add_argument(
            "--activities-per-user",
            type=int,
            help="Number of activities to add for each user",
            default=10,
        )
        parser.add_argument(
            "--moods-per-user",
            type=int,
            help="Number of moods to add for each user",
            default=500,
        )

    def handle(self, *args, **options):
        num_users = options.get("users")
        activities_per_user = options.get("activities_per_user")
        moods_per_user = options.get("moods_per_user")

        users = []
        for _ in range(num_users):
            users.append(
                get_user_model().objects.create_user(
                    username=fake.name(),
                    email=fake.email(),
                    password=fake.password(),
                )
            )

        activities = []
        for user in users:
            random_activities = random.sample(
                DUMMY_ACTIVITIES, min(activities_per_user, len(DUMMY_ACTIVITIES))
            )
            activities.extend(
                [Activity(user=user, name=name) for name in random_activities]
            )
        Activity.objects.bulk_create(activities)

        moods = []
        for user in users:
            user_activities = Activity.objects.filter(user=user)
            for _ in range(moods_per_user):
                mood = Mood(
                    user=user,
                    mood=random.choice(Mood.MOOD_CHOICES)[0],
                    note_title=fake.sentence(),
                    note=fake.paragraph(),
                    date=fake.date_between(start_date="-1y"),
                    time=fake.date_time_between(start_date="-1y"),
                )
                mood.save()
                mood.activities.set(
                    random.sample(
                        list(user_activities), random.randint(1, len(user_activities))
                    )
                )
                moods.append(mood)

        self.stdout.write(self.style.SUCCESS("Database seeded successfully."))
