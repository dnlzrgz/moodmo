from django.db import models
from django.conf import settings
from django.urls import reverse


class Activity(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=50)
    last_modified = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse("activity_edit", kwargs={"pk": self.pk})

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name_plural = "activities"
