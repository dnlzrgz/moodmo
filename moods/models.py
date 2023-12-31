from django.db import models
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField
from django.conf import settings
from django.utils import timezone
from django.urls import reverse


class Activity(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name_plural = "activities"


class Mood(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    MOOD_CHOICES = [
        (-2, "very unhappy"),
        (-1, "unhappy"),
        (0, "neutral"),
        (1, "happy"),
        (2, "very happy"),
    ]
    mood = models.IntegerField(choices=MOOD_CHOICES)
    note_title = models.CharField(blank=True, max_length=255)
    note = models.TextField(blank=True)
    activities = models.ManyToManyField(
        Activity,
        related_name="moods",
        blank=True,
    )
    timestamp = models.DateTimeField(default=timezone.now)
    last_modified = models.DateTimeField(auto_now=True)

    search_vector = SearchVectorField(null=True)

    def get_absolute_url(self):
        return reverse("mood_detail", kwargs={"pk": self.pk})

    def __str__(self) -> str:
        return f"Mood added on {self.timestamp}"

    class Meta:
        indexes = [
            GinIndex(fields=["search_vector"]),
        ]
