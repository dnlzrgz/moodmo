from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    TemplateView,
    UpdateView,
    DeleteView,
)
from moods.forms import MoodForm
from moods.mixins import UserIsOwnerMixin, SetUserMixin
from moods.models import Mood


class MoodListView(LoginRequiredMixin, ListView):
    model = Mood
    template_name = "moods/mood_list.html"
    context_object_name = "moods"
    paginate_by = 30

    def get(self, request, *args, **kwargs):
        if request.headers.get("HX-Request"):
            self.template_name = "moods/hx_mood_list.html"
        else:
            self.template_name = "moods/mood_list.html"

        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return Mood.objects.filter(user=self.request.user).prefetch_related(
            "activities"
        )


class MoodSearchView(LoginRequiredMixin, TemplateView):
    template_name = "moods/mood_search.html"


class MoodSearchResultsView(LoginRequiredMixin, ListView):
    model = Mood
    template_name = "moods/hx_mood_list.html"
    context_object_name = "moods"
    paginate_by = 30

    def get(self, request, *args, **kwargs):
        if not request.headers.get("HX-Request"):
            return redirect("mood_search")

        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        mood = self.request.GET.get("mood", "")
        search_term = self.request.GET.get("search_term", "")
        start_date = self.request.GET.get("start_date", "")
        end_date = self.request.GET.get("end_date", "")

        moods = Mood.objects.filter(user=self.request.user)

        if mood:
            moods = moods.filter(mood=mood)
        if search_term:
            moods = moods.filter(search_vector=search_term)
        if start_date:
            start_date = make_aware(datetime.strptime(start_date, "%Y-%m-%d"))
            moods = moods.filter(date__gte=start_date - timedelta(days=1))
        if end_date:
            end_date = make_aware(datetime.strptime(end_date, "%Y-%m-%d"))
            moods = moods.filter(date__lte=end_date + timedelta(days=1))

        moods = moods.prefetch_related("activities")
        return moods


class MoodCreateView(LoginRequiredMixin, SetUserMixin, CreateView):
    model = Mood
    form_class = MoodForm
    template_name = "moods/mood_create.html"
    success_url = reverse_lazy("mood_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class MoodUpdateView(LoginRequiredMixin, UserIsOwnerMixin, SetUserMixin, UpdateView):
    model = Mood
    form_class = MoodForm
    template_name = "moods/mood_update.html"
    success_url = reverse_lazy("mood_list")
    slug_field = "sqid"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class MoodDeleteView(LoginRequiredMixin, UserIsOwnerMixin, DeleteView):
    model = Mood
    template_name = "moods/mood_delete.html"
    success_url = reverse_lazy("mood_list")
    context_object_name = "mood"
    slug_field = "sqid"
