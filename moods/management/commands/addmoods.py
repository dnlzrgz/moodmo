import random

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from faker import Faker

from moods.models import Mood

fake = Faker()


class Command(BaseCommand):
    help = "Add random moods."

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            "-n",
            type=int,
            help="Number of moods to add",
        )
        parser.add_argument(
            "--username",
            "-u",
            type=str,
            help="Specify user name to add moods to",
        )

    def handle(self, *args, **options):
        user_queryset = get_user_model().objects.all()
        n = options.get("number")
        username = options.get("username")

        if username:
            user_queryset = user_queryset.filter(username=username)

        random_entries = [
            Mood(
                user=random.choice(user_queryset),
                mood=random.choice(Mood.MOOD_CHOICES)[0],
                note_title=fake.sentence(),
                note=fake.paragraph(),
            )
            for _ in range(n)
        ]

        Mood.objects.bulk_create(random_entries)
        self.stdout.write(self.style.SUCCESS("moods added to the database."))
