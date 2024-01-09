import csv
from typing import Any
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    FormView,
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)
from moods.forms import MoodForm, UploadFileForm
from moods.mixins import UserIsOwnerMixin, SetUserMixin
from moods.models import Mood


class MoodListView(LoginRequiredMixin, ListView):
    model = Mood
    template_name = "moods/mood_list.html"


class MoodInfiniteListView(LoginRequiredMixin, ListView):
    model = Mood
    context_object_name = "moods"
    paginate_by = 24

    def dispatch(self, request, *args, **kwargs):
        if "X-Alpine-Load" not in request.headers:
            return HttpResponseForbidden("Forbidden: Direct access not allowed.")

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self) -> QuerySet[Any]:
        ordering = self.request.GET.get("ordering", "-timestamp")
        queryset = Mood.objects.filter(user=self.request.user).order_by(ordering)
        return queryset

    def render_to_response(self, context, **kwargs):
        moods = [
            {
                "id": mood.id,
                "mood": mood.mood,
                "note_title": mood.note_title,
                "note": mood.note,
                "timestamp": mood.timestamp,
            }
            for mood in context["moods"]
        ]

        return JsonResponse({"moods": moods})


class MoodSearchView(LoginRequiredMixin, ListView):
    model = Mood
    context_object_name = "moods"

    def dispatch(self, request, *args, **kwargs):
        if "X-Alpine-Search" not in request.headers:
            return HttpResponseForbidden("Forbidden: Direct access not allowed.")

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        query = self.request.GET.get("q")
        limit = self.request.GET.get("limit", 10)

        limit = max(1, min(int(limit), 20))

        return Mood.objects.filter(
            search_vector=query, user=self.request.user
        ).order_by("-timestamp")[:limit]

    def render_to_response(self, context, **kwargs):
        mood_data = [
            {
                "id": mood.id,
                "note_title": mood.note_title,
                "note": mood.note,
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


class MoodImportView(LoginRequiredMixin, FormView):
    form_class = UploadFileForm
    template_name = "moods/mood_import.html"
    success_url = reverse_lazy("mood_list")

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        file = form.cleaned_data["file"]
        print("--------------------------------------")
        print(file)
        print("--------------------------------------")

        return super().form_valid(form)


class MoodExportView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        moods = Mood.objects.filter(user=self.request.user).order_by("-timestamp")
        export_format = self.request.GET.get("format", "csv")

        if export_format == "json":
            mood_data = [
                {
                    "mood": mood.mood,
                    "note_title": mood.note_title,
                    "note": mood.note,
                    "timestamp": mood.timestamp,
                }
                for mood in moods
            ]

            return JsonResponse({"moods": mood_data})
        else:
            response = HttpResponse(content_type="text/csv")
            response["Content-Disposition"] = 'attachment; filename="moods_export.csv"'

            writer = csv.writer(response)
            writer.writerow(["mood", "note_title", "note", "timestamp"])

            writer.writerows(
                [
                    [mood.mood, mood.note_title, mood.note, mood.timestamp]
                    for mood in moods
                ]
            )

            return response
