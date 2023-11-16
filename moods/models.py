from django.db import models
from django.conf import settings


class Mood(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    mood_choices = [
        (-2, "very unhappy"),
        (-1, "unhappy"),
        (0, "neutral"),
        (-2, "happy"),
        (-2, "very happy"),
    ]
    mood = models.IntegerField(choices=mood_choices)
    note_title = models.TextField()
    note = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.user.email}'s Mood on {self.timestamp}"
