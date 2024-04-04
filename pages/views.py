from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView


class HomePageView(TemplateView):
    template_name = "pages/home.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("mood_list")

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["canonical_url"] = settings.CANONICAL_URL
        return context


class SettingsView(LoginRequiredMixin, TemplateView):
    template_name = "pages/settings.html"


class StatisticsPageView(LoginRequiredMixin, TemplateView):
    template_name = "pages/statistics.html"
