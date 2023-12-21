from django.urls import path
from .views import (
    MoodListView,
    MoodSearchView,
    MoodCreateView,
    MoodUpdateView,
    MoodDeleteView,
)

urlpatterns = [
    path(
        "",
        MoodListView.as_view(),
        name="mood_list",
    ),
    path(
        "search/",
        MoodSearchView.as_view(),
        name="mood_search",
    ),
    path(
        "create/",
        MoodCreateView.as_view(),
        name="mood_create",
    ),
    path(
        "edit/<int:pk>",
        MoodUpdateView.as_view(),
        name="mood_edit",
    ),
    path(
        "delete/<int:pk>",
        MoodDeleteView.as_view(),
        name="mood_delete",
    ),
]
