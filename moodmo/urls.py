from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from moodmo.api import api

urlpatterns = [
    path(settings.DJANGO_ADMIN_URL, admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("moods/", include("moods.urls")),
    path("activities/", include("activities.urls")),
    path("api/v1/", api.urls),
    path("", include("pages.urls")),
]

if settings.DEBUG:
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
        path("__reload__/", include("django_browser_reload.urls")),
    ]
