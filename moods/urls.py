from django.urls import path
from .views import (
    MoodListView,
    MoodCreateView,
    MoodUpdateView,
    MoodDeleteView,
    MoodSearchView,
    MoodSearchResultsView,
)

urlpatterns = [
    path(
        "",
        MoodListView.as_view(),
        name="mood_list",
    ),
    path(
        "create/",
        MoodCreateView.as_view(),
        name="mood_create",
    ),
    path(
        "edit/<slug>",
        MoodUpdateView.as_view(),
        name="mood_edit",
    ),
    path(
        "delete/<slug>",
        MoodDeleteView.as_view(),
        name="mood_delete",
    ),
    path(
        "search/",
        MoodSearchView.as_view(),
        name="mood_search",
    ),
    path(
        "search/results/",
        MoodSearchResultsView.as_view(),
        name="mood_search_results",
    ),
]
