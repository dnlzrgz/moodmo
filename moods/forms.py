from django import forms
from .models import Mood


class MoodForm(forms.ModelForm):
    class Meta:
        model = Mood
        fields = [
            "mood",
            "note_title",
            "note",
            # "activities",
            "timestamp",
        ]


class UploadFileForm(forms.Form):
    file = forms.FileField()


class ExportOptionsForm(forms.Form):
    export_format = forms.ChoiceField(
        choices=[
            ("csv", "CSV"),
            ("json", "JSON"),
        ],
    )
