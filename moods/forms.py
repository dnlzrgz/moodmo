from django import forms
from moods.models import Activity, Mood


class ActivityForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Name of the activity",
            },
        ),
    )

    class Meta:
        model = Activity
        fields = ["name"]


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
    activities = forms.ModelMultipleChoiceField(
        queryset=None,
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Mood
        fields = [
            "mood",
            "note_title",
            "note",
            "activities",
            "date",
            "time",
        ]

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["activities"].queryset = Activity.objects.filter(user=user)


class UploadFileForm(forms.Form):
    file = forms.FileField()


class ExportOptionsForm(forms.Form):
    export_format = forms.ChoiceField(
        choices=[
            ("csv", "CSV"),
            ("json", "JSON"),
        ],
    )
