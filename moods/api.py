from ninja import Router
from typing import List
from ninja.pagination import paginate, PageNumberPagination
from .models import Mood
from .schemas import MoodSchema


router = Router()


@router.get("/list", response=List[MoodSchema])
@paginate(PageNumberPagination)
def list(request):
    return Mood.objects.filter(user=request.user).order_by("-timestamp")


@router.get("/search", response=List[MoodSchema])
def search(request, q: str = "", limit: int = 7):
    return Mood.objects.filter(search_vector=q, user=request.user).order_by(
        "-timestamp"
    )[:limit]
