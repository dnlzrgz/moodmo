from django.shortcuts import redirect
from django.views.generic import TemplateView


class HomePageView(TemplateView):
    template_name = "pages/home.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("mood_list")

        return super().dispatch(request, *args, **kwargs)
