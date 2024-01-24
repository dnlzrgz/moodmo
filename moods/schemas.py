from ninja import ModelSchema
from .models import Mood


class MoodSchema(ModelSchema):
    class Meta:
        model = Mood
        fields = [
            "id",
            "mood",
            "note_title",
            "note",
            "activities",
            "timestamp",
        ]
