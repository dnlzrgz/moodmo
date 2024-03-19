import csv
import json
from django.conf import settings
from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import FormView, TemplateView
from settings.forms import (
    UploadFileForm,
    ExportOptionsForm,
)
from moods.models import Mood
from activities.models import Activity


class SettingsView(LoginRequiredMixin, TemplateView):
    template_name = "settings/settings.html"


class ImportView(LoginRequiredMixin, FormView):
    form_class = UploadFileForm
    template_name = "settings/import.html"
    success_url = reverse_lazy("mood_list")
    max_upload_size = settings.FILE_UPLOAD_MAX_MEMORY_SIZE

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        file = form.cleaned_data["file"]

        if not (
            file.name.endswith(".csv") or file.name.endswith(".json")
        ) or file.content_type not in ["text/csv", "application/json"]:
            form.add_error("file", "Only CSV or JSON files are supported.")
            return self.form_invalid(form)

        if file.size > self.max_upload_size:
            form.add_error(
                "file",
                "The file is too big. The maximum support filesize is 2.5 MB.",
            )
            return self.form_invalid(form)

        try:
            if file.name.endswith(".csv"):
                self.import_csv(file)
            elif file.name.endswith(".json"):
                self.import_json(file)
        except (csv.Error, json.JSONDecodeError, KeyError, ValueError) as e:
            form.add_error("file", f"Error reading or parsing file: {e}")
            return self.form_invalid(form)

        return super().form_valid(form)

    def import_csv(self, file):
        csv_data = file.read().decode("utf-8")
        csv_reader = csv.DictReader(csv_data.splitlines())
        for row in csv_reader:
            activities = [
                Activity.objects.get_or_create(
                    user=self.request.user,
                    name=activity.strip(),
                )[0]
                for activity in row["activities"].split(", ")
            ]

            mood = Mood.objects.create(
                user=self.request.user,
                mood=row["mood"],
                note_title=row["note_title"],
                note=row["note"],
                timestamp=timezone.datetime.strptime(
                    row["timestamp"],
                    "%Y-%m-%d %H:%M:%S %z",
                ),
            )
            mood.activities.set(activities)

    def import_json(self, file):
        with transaction.atomic():
            json_data = json.loads(file.read().decode("utf-8"))
            for item in json_data:
                mood = Mood.objects.create(
                    user=self.request.user,
                    mood=item["mood"],
                    note_title=item["note_title"],
                    note=item["note"],
                    timestamp=timezone.datetime.strptime(
                        item["timestamp"], "%Y-%m-%d %H:%M:%S %z"
                    ),
                )

                activities = item.get("activities", [])
                for name in activities:
                    activity, _ = Activity.objects.get_or_create(
                        user=self.request.user,
                        name=name,
                    )

                    mood.activities.add(activity)


class ExportView(LoginRequiredMixin, FormView):
    form_class = ExportOptionsForm
    template_name = "settings/export.html"
    success_url = reverse_lazy("mood_list")

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.create_export(form.cleaned_data["export_format"])

        return self.form_invalid(form)

    def create_export(self, export_format):
        moods = (
            Mood.objects.filter(user=self.request.user)
            .order_by("-timestamp")
            .prefetch_related("activities")
        )

        if export_format == "json":
            return self.export_json(moods)
        else:
            return self.export_csv(moods)

    def export_json(self, moods):
        mood_data = [
            {
                "mood": mood.mood,
                "note_title": mood.note_title,
                "note": mood.note,
                "activities": [activity.name for activity in mood.activities.all()],
                "timestamp": mood.timestamp.strftime("%Y-%m-%d %H:%M:%S %z"),
            }
            for mood in moods
        ]

        current_date = timezone.now().strftime("%Y_%m_%d")
        response = JsonResponse(mood_data, safe=False)
        response["Content-Disposition"] = (
            f'attachment; filename="moodmo_export_{current_date}.json"'
        )
        return response

    def export_csv(self, moods):
        current_date = timezone.now().strftime("%Y_%m_%d")
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = (
            f'attachment; filename="moodmo_export_{current_date}.csv"'
        )

        writer = csv.writer(response)
        writer.writerow(["mood", "note_title", "note", "activities", "timestamp"])
        for mood in moods:
            writer.writerow(
                {
                    "mood": mood.mood,
                    "note_title": mood.note_title,
                    "note": mood.note,
                    "activities": ", ".join(
                        [activity.name for activity in mood.activities.all()]
                    ),
                    "timestamp": mood.timestamp.strftime("%Y-%m-%d %H:%M:%S %z"),
                }
            )
        return response
