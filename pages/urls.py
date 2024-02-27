from django.urls import path
from django.views.generic.base import TemplateView
from pages.views import HomePageView, SettingsPageView, StatisticsPageView

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
        "stats",
        StatisticsPageView.as_view(),
        name="statistics",
    ),
    path(
        "robots.txt",
        TemplateView.as_view(
            template_name="pages/robots.txt",
            content_type="text/plain",
        ),
        name="robots",
    ),
    path(
        "sitemap.xml",
        TemplateView.as_view(
            template_name="pages/sitemap.xml",
            content_type="text/xml",
        ),
        name="sitemap",
    ),
]
