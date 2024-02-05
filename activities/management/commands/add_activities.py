import random
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from activities.models import Activity

DUMMY_ACTIVITIES = [
    "Art and Craft",
    "Biking",
    "Board Games",
    "Botanical Garden Visit",
    "Camping",
    "Cooking Class",
    "Cooking",
    "Crafting",
    "DIY Planter Workshop",
    "Dancing",
    "Exercise",
    "Flower Arranging",
    "Gaming",
    "Gardening",
    "Hiking",
    "Indoor Gardening",
    "Learning a New Skill",
    "Listening to Music",
    "Meditation",
    "Mindfulness Activities",
    "Nature Photography",
    "Nature Walk",
    "Photography",
    "Plant Swap",
    "Play with Pets",
    "Podcast Listening",
    "Reading",
    "Socializing with Friends",
    "Swimming",
    "Terrarium Making",
    "Traveling",
    "Visit a Museum",
    "Visit a National Park",
    "Visit a Park",
    "Volunteering",
    "Wine Tasting",
    "Winter Sports",
    "Writing",
]


class Command(BaseCommand):
    help = "Add activities."

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            "-n",
            type=int,
            help="Number of activities to add",
            default=len(DUMMY_ACTIVITIES),
        )

        parser.add_argument(
            "--username",
            "-u",
            type=str,
            help="Specify user name to add activities to",
        )

    def handle(self, *args, **options):
        user_queryset = get_user_model().objects.all()
        username = options.get("username")
        n = options.get("number")

        if username:
            user_queryset = user_queryset.filter(username=username)

        random_activities = random.sample(
            DUMMY_ACTIVITIES, min(n, len(DUMMY_ACTIVITIES))
        )

        # Create activities
        activities = [
            Activity(
                user=random.choice(user_queryset),
                name=dummy,
            )
            for dummy in random_activities
        ]
        Activity.objects.bulk_create(activities)

        self.stdout.write(self.style.SUCCESS("Activities added to the database."))
