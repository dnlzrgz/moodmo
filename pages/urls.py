from django.urls import path
from django.views.generic.base import TemplateView
from pages.views import HomePageView, SettingsPageView

urlpatterns = [
    path(
        "",
        HomePageView.as_view(),
        name="home",
    ),
    path(
        "settings",
        SettingsPageView.as_view(),
        name="settings",
    ),
    path(
        "robots.txt",
        TemplateView.as_view(
            template_name="pages/robots.txt",
            content_type="text/plain",
        ),
        name="robots",
    ),
]
