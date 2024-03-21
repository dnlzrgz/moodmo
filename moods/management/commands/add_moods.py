import random
from datetime import datetime
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from moods.models import Mood
from activities.models import Activity

try:
    from faker import Faker

    fake = Faker()
except ImportError:
    raise ImportError(
        "Faker package is required for this command. Maybe you're in the wrong environment."
    )


class Command(BaseCommand):
    help = "Add random moods."

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            "-n",
            type=int,
            help="Number of moods to add",
            default=100,
        )
        parser.add_argument(
            "--username",
            "-u",
            type=str,
            help="Specify user name to add moods to",
        )
        parser.add_argument(
            "--start-date",
            type=str,
            help="Start date for range of dates (format: YYYY-MM-DD)",
            default=datetime.today().strftime("%Y-%m-%d"),
        )
        parser.add_argument(
            "--end-date",
            type=str,
            help="End date for range of dates (format: YYYY-MM-DD)",
            default=datetime.today().strftime("%Y-%m-%d"),
        )

    def handle(self, *args, **options):
        user_queryset = get_user_model().objects.all()
        n = options.get("number")
        username = options.get("username")
        start_date = datetime.strptime(options.get("start_date"), "%Y-%m-%d")
        end_date = datetime.strptime(options.get("end_date"), "%Y-%m-%d")

        if username:
            user_queryset = user_queryset.filter(username=username)

        # Create moods
        moods = []
        for _ in range(n):
            fake_dt = fake.date_time_between_dates(
                datetime_start=start_date,
                datetime_end=end_date,
                tzinfo=timezone.get_current_timezone(),
            )
            moods.append(
                Mood(
                    user=random.choice(user_queryset),
                    mood=random.choice(Mood.MOOD_CHOICES)[0],
                    note_title=fake.sentence(),
                    note=fake.paragraph(),
                    date=fake_dt.date(),
                    time=fake_dt.time(),
                )
            )

        Mood.objects.bulk_create(moods)

        # Check if there are any activites
        activities = Activity.objects.all()
        if activities.exists():
            for mood in moods:
                activities_to_add = random.randint(0, activities.count())
                random_activities = random.sample(list(activities), activities_to_add)
                mood.activities.add(
                    *Activity.objects.filter(name__in=random_activities)
                )

        self.stdout.write(self.style.SUCCESS("Moods added to the database."))
