from django import forms
from moods.models import Mood
from activities.models import Activity

from django.core.exceptions import ValidationError

MAX_SIZE_LIMIT = 2.5 * 1024 * 1024  # 2.5 MB


def bytes_to_megabytes(bytes_value):
    megabytes = round(bytes_value / (1024**2), 2)
    return megabytes


def validate_file_size(value):
    if value.size > MAX_SIZE_LIMIT:
        raise ValidationError(
            f"File is too large: {bytes_to_megabytes(value.size)} MB. Size should not exceed {bytes_to_megabytes(MAX_SIZE_LIMIT)} MB."
        )


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
        queryset=Activity.objects.none(),
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
            "timestamp",
        ]

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["activities"].queryset = Activity.objects.filter(user=user)


class UploadFileForm(forms.Form):
    file = forms.FileField(
        validators=[validate_file_size],
    )


class ExportOptionsForm(forms.Form):
    export_format = forms.ChoiceField(
        choices=[
            ("csv", "CSV"),
            ("json", "JSON"),
        ],
    )
