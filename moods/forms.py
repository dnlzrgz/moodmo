from django import forms
from .models import Mood


class MoodForm(forms.ModelForm):
    note_title = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Add a quick summary",
            },
        ),
        required=False,
    )
    note = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "placeholder": "Add a note",
            },
        ),
        required=False,
    )

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
