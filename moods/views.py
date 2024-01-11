import csv
import json
from datetime import datetime
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

        # Check that file is a CSV
        if not (file.name.endswith(".csv") or file.name.endswith(".json")):
            form.add_error("file", "Only CSV or JSON files are allowed.")
            return self.form_invalid(form)

        try:
            if file.name.endswith(".csv"):
                csv_data = file.read().decode("utf-8")
                csv_reader = csv.DictReader(csv_data.splitlines())
                moods = [
                    Mood(
                        user=self.request.user,
                        mood=row["mood"],
                        note_title=row["note_title"],
                        note=row["note"],
                        timestamp=row["timestamp"],
                    )
                    for row in csv_reader
                ]

                Mood.objects.bulk_create(moods)

            elif file.name.endswith(".json"):
                pass

        except (csv.Error, json.JSONDecodeError) as e:
            form.add_error("file", f"Error reading file: {e}")
            return self.form_invalid(form)

        return super().form_valid(form)


class MoodExportView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        moods = Mood.objects.filter(user=self.request.user).order_by("-timestamp")
        export_format = self.request.GET.get("format", "csv")

        if export_format == "json":
            pass
        else:
            response = HttpResponse(content_type="text/csv")
            current_date = datetime.now().strftime("%Y_%m_%d")
            response[
                "Content-Disposition"
            ] = f'attachment; filename="moodmo_export_{current_date}.csv"'

            writer = csv.writer(response)
            writer.writerow(["mood", "note_title", "note", "timestamp"])

            writer.writerows(
                [
                    [mood.mood, mood.note_title, mood.note, mood.timestamp]
                    for mood in moods
                ]
            )

            return response
