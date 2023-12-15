from django.urls import path
from .views import (
    MoodListView,
    MoodCreateView,
    MoodUpdateView,
    MoodDetailView,
    MoodDeleteView,
)

urlpatterns = [
    path(
        "",
        MoodListView.as_view(),
        name="mood_list",
    ),
    path(
        "details/<int:pk>/",
        MoodDetailView.as_view(),
        name="mood_detail",
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
