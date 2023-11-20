from django.urls import path
from .views import (
    MoodListView,
    MoodCreateView,
    MoodUpdateView,
    MoodDetailView,
    MoodDeleteView,
)

urlpatterns = [
    path("", MoodListView.as_view(), name="mood_list"),
    path("<int:pk>/", MoodDetailView.as_view(), name="mood_detail"),
    path("add/", MoodCreateView.as_view(), name="mood_add"),
    path("<int:pk>/edit/", MoodUpdateView.as_view(), name="mood_edit"),
    path("<int:pk>/delete/", MoodDeleteView.as_view(), name="mood_delete"),
]
