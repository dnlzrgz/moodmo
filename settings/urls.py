from django.urls import path
from settings.views import (
    SettingsView,
    ExportView,
    ImportView,
)

urlpatterns = [
    path(
        "",
        SettingsView.as_view(),
        name="settings",
    ),
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
