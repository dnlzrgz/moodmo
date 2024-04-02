from django.urls import path
from django.views.generic.base import TemplateView
from django.views.decorators.cache import cache_page
from pages.views import (
    HomePageView,
    StatisticsPageView,
)

urlpatterns = [
    path(
        "",
        cache_page(60 * 15)(HomePageView.as_view()),
        name="home",
    ),
    path(
        "stats",
        StatisticsPageView.as_view(),
        name="statistics",
    ),
    path(
        "robots.txt",
        cache_page(60 * 15)(
            TemplateView.as_view(
                template_name="pages/robots.txt",
                content_type="text/plain",
            ),
        ),
        name="robots",
    ),
]
