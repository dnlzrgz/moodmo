from ninja import NinjaAPI, Swagger
from typing import List
from ninja.pagination import paginate, PageNumberPagination
from ninja.security import django_auth
from django.contrib.admin.views.decorators import staff_member_required
from .models import Mood
from .schemas import MoodSchema


api = NinjaAPI(
    version="1.0.0",
    auth=django_auth,
    docs=Swagger(),
    docs_decorator=staff_member_required,
)


@api.get("/list", response=List[MoodSchema])
@paginate(PageNumberPagination)
def list(request):
    return Mood.objects.filter(user=request.user).order_by("-timestamp")


@api.get("/search", response=List[MoodSchema])
def search(request, q: str = "", limit: int = 7):
    return Mood.objects.filter(search_vector=q, user=request.user).order_by(
        "-timestamp"
    )[:limit]
