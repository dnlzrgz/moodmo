from ninja import ModelSchema
from activities.models import Activity


class ActivitySchema(ModelSchema):
    class Meta:
        model = Activity
        fields = ["name"]
