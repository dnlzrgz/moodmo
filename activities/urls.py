from django.urls import path
from activities.views import (
    ActivityListView,
    ActivityCreateView,
    ActivityUpdateView,
    ActivityDeleteView,
)

urlpatterns = [
    path(
        "",
        ActivityListView.as_view(),
        name="activity_list",
    ),
    path(
        "create/",
        ActivityCreateView.as_view(),
        name="activity_create",
    ),
    path(
        "edit/<int:pk>",
        ActivityUpdateView.as_view(),
        name="activity_edit",
    ),
    path(
        "delete/<int:pk>",
        ActivityDeleteView.as_view(),
        name="activity_delete",
    ),
]
