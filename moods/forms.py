from django import forms
from moods.models import Mood
from activities.models import Activity


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
            "date",
            "time",
        ]

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["activities"].queryset = Activity.objects.filter(user=user)
