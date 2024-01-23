from django import forms
from activities.models import Activity


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
