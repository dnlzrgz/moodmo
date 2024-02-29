from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class AccountDeleteView(LoginRequiredMixin, TemplateView):
    template_name = "pages/delete_account.html"

    def post(self, request, *args, **kwargs):
        user = request.user
        logout(request)  # logout before deleting

        user.delete()
        return redirect("home")
