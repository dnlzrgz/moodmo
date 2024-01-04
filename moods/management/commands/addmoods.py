import random
from datetime import datetime
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker

from moods.models import Activity, Mood

fake = Faker()

ACTIVITY_CHOICES = [
    "meditating",
    "running",
    "reading",
    "listening to music",
    "painting",
    "cooking",
    "gardening",
    "yoga",
    "swimming",
    "hiking",
    "cycling",
    "writing",
    "photography",
    "watching movies",
    "gaming",
    "dancing",
    "traveling",
    "singing",
    "volunteering",
    "coding",
]


class Command(BaseCommand):
    help = "Add random moods."

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            "-n",
            type=int,
            help="Number of moods to add",
            default="100",
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

        # Create activities
        activities = [
            Activity(
                user=random.choice(user_queryset),
                name=activity,
            )
            for activity in ACTIVITY_CHOICES
        ]
        Activity.objects.bulk_create(activities)

        # Create moods
        moods = [
            Mood(
                user=random.choice(user_queryset),
                mood=random.choice(Mood.MOOD_CHOICES)[0],
                note_title=fake.sentence(),
                note=fake.paragraph(),
                timestamp=fake.date_time_between(
                    start_date=start_date,
                    end_date=end_date,
                    tzinfo=timezone.get_current_timezone(),
                ),
            )
            for _ in range(n)
        ]
        Mood.objects.bulk_create(moods)

        # Update some moods with activities
        all_moods = Mood.objects.all()
        selected_moods = random.sample(list(all_moods), int(0.5 * n))

        for mood in selected_moods:
            num_activities = random.randint(0, len(activities))
            selected_activities = random.sample(activities, num_activities)
            mood.activities.set(selected_activities)

            mood.save()

        self.stdout.write(self.style.SUCCESS("Moods added to the database."))
