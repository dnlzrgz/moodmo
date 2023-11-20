from django.forms import ModelForm
from .models import Mood


class MoodForm(ModelForm):
    pass

    class Meta:
        model = Mood
        fields = [
            "mood",
            "note_title",
            "note",
            "timestamp",
        ]
