"""
URL configuration for moodmo project.
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView

urlpatterns = [
    path("management/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path(
        "",
        TemplateView.as_view(template_name="home.html"),
        name="home",
    ),
]

if settings.DEBUG:
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]
