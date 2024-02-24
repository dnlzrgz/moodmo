from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class HomePageView(TemplateView):
    template_name = "pages/home.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("mood_list")

        return super().dispatch(request, *args, **kwargs)


class SettingsPageView(LoginRequiredMixin, TemplateView):
    template_name = "pages/settings.html"


class StatisticsPageView(LoginRequiredMixin, TemplateView):
    template_name = "pages/statistics.html"
