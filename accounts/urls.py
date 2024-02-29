from django.urls import path
from accounts.views import AccountDeleteView

urlpatterns = [
    path(
        "delete-account",
        AccountDeleteView.as_view(),
        name="account_delete",
    ),
]
