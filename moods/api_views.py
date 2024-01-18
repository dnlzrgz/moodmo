from ninja import NinjaAPI, Redoc
from ninja.pagination import paginate, PageNumberPagination
from ninja.security import django_auth
from django.contrib.admin.views.decorators import staff_member_required
from .models import Mood
from .schemas import MoodSchema


api = NinjaAPI(
    version="1.0.0",
    auth=django_auth,
    docs=Redoc(),
    docs_decorator=staff_member_required,
)


@api.get(
    "/list",
    response=list[MoodSchema],
)
@paginate(PageNumberPagination)
def list(request):
    return Mood.objects.filter(user=request.user).order_by("-timestamp")
