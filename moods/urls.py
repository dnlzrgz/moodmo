from django.urls import path
from moods.views import (
    ActivityListView,
    ActivityCreateView,
    ActivityUpdateView,
    ActivityDeleteView,
    MoodListView,
    MoodCreateView,
    MoodUpdateView,
    MoodDeleteView,
    MoodSearchView,
    ExportView,
    ImportView,
)

moods_urlpatterns = [
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
]

activities_urlpatterns = [
    path(
        "activities/",
        ActivityListView.as_view(),
        name="activity_list",
    ),
    path(
        "activities/create/",
        ActivityCreateView.as_view(),
        name="activity_create",
    ),
    path(
        "activities/edit/<slug>",
        ActivityUpdateView.as_view(),
        name="activity_edit",
    ),
    path(
        "activities/delete/<slug>",
        ActivityDeleteView.as_view(),
        name="activity_delete",
    ),
]

export_and_import_urlpatterns = [
    path(
        "export/",
        ExportView.as_view(),
        name="export",
    ),
    path(
        "import/",
        ImportView.as_view(),
        name="import",
    ),
]

urlpatterns = moods_urlpatterns + activities_urlpatterns + export_and_import_urlpatterns
