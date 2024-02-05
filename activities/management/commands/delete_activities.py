from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from activities.models import Activity


class Command(BaseCommand):
    help = "Delete activities."

    def add_arguments(self, parser):
        parser.add_argument(
            "--username",
            "-u",
            type=str,
            help="Specify user name to remove moods from",
        )

    def handle(self, *args, **options):
        username = options.get("username")

        if username:
            user_queryset = get_user_model().objects.filter(username=username)

            if not user_queryset.exists():
                self.stderr.write(
                    self.style.ERROR(f"User with username '{username}' not found.")
                )
                return

            activities_to_delete = Activity.objects.filter(user=user_queryset.first())
        else:
            activities_to_delete = Activity.objects.all()

        activities_to_delete.delete()

        if username:
            self.stdout.write(
                self.style.SUCCESS(
                    f"Activities for user '{username}' removed from the database."
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS("All activities removed from the database.")
            )
