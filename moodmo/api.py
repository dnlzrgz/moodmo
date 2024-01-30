from ninja import NinjaAPI, Swagger
from ninja.security import django_auth
from django.contrib.admin.views.decorators import staff_member_required

api = NinjaAPI(
    version="1.0.0",
    auth=django_auth,
    docs=Swagger(),
    docs_decorator=staff_member_required,
)

api.add_router("/moods/", "moods.api.router", tags=["moods"])
