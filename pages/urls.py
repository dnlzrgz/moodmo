from django.urls import path
from django.views.generic.base import TemplateView
from pages.views import (
    HomePageView,
    StatisticsPageView,
)

urlpatterns = [
    path(
        "",
        HomePageView.as_view(),
        name="home",
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
]
