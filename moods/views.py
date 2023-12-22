from typing import Any
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
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
    paginate_by = 24

    def get_queryset(self) -> QuerySet[Any]:
        ordering = self.request.GET.get("ordering", "-timestamp")
        queryset = Mood.objects.filter(user=self.request.user).order_by(ordering)
        return queryset


class MoodSearchView(LoginRequiredMixin, ListView):
    model = Mood
    context_object_name = "moods"

    def get_queryset(self):
        query = self.request.GET.get("q")
        limit = self.request.GET.get("limit", 10)
        search_vector = SearchVector("note_title", "note")
        search_query = SearchQuery(query)

        limit = max(1, min(int(limit), 100))

        return Mood.objects.annotate(
            search=search_vector,
            rank=SearchRank(search_vector, search_query),
        ).filter(search=search_query, user=self.request.user)[:limit]

    def render_to_response(self, context, **kwargs):
        mood_data = [
            {
                "id": mood.id,
                "note_title": mood.note_title,
                "timestamp": mood.timestamp,
            }
            for mood in context["moods"]
        ]
        return JsonResponse({"moods": mood_data})


class MoodCreateView(LoginRequiredMixin, SetUserMixin, CreateView):
    model = Mood
    form_class = MoodForm
    template_name = "moods/mood_create.html"
    success_url = reverse_lazy("mood_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class MoodUpdateView(LoginRequiredMixin, UserIsOwnerMixin, SetUserMixin, UpdateView):
    model = Mood
    form_class = MoodForm
    template_name = "moods/mood_update.html"
    success_url = reverse_lazy("mood_list")


class MoodDeleteView(LoginRequiredMixin, UserIsOwnerMixin, DeleteView):
    model = Mood
    template_name = "moods/mood_delete.html"
    success_url = reverse_lazy("mood_list")
    context_object_name = "mood"
