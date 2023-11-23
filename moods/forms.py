from django import forms
from .models import Mood


class MoodForm(forms.ModelForm):
    pass

    class Meta:
        model = Mood
        fields = [
            "mood",
            "note_title",
            "note",
            "timestamp",
        ]
