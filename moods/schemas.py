from typing import List
from ninja import ModelSchema
from moods.models import Mood
from activities.schemas import ActivitySchema


class MoodSchema(ModelSchema):
    activities: List[ActivitySchema]

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
