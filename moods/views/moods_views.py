import csv
import json
from datetime import datetime, timedelta
from django.conf import settings
from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    TemplateView,
    UpdateView,
    DeleteView,
    FormView,
)
from utils.mixins import UserIsOwnerMixin, SetUserMixin
from moods.forms import MoodForm, UploadFileForm, ExportOptionsForm
from moods.models import Activity, Mood


class MoodListView(LoginRequiredMixin, ListView):
    model = Mood
    template_name = "moods/mood_list.html"
    context_object_name = "moods"
    paginate_by = 30

    def get(self, request, *args, **kwargs):
        self.template_name = "moods/mood_list.html"

        if request.headers.get("HX-Request"):
            self.template_name = "moods/hx_mood_list.html"
        else:
            self.template_name = "moods/mood_list.html"

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        date = self.request.GET.get("date")

        try:
            if date is None:
                current_date = timezone.now().date()
            else:
                current_date = datetime.strptime(date, "%Y-%m").date()

        except ValueError:
            current_date = timezone.now().date()

        context["prev_month"] = current_date.replace(day=1) - timedelta(days=1)
        context["current_month"] = current_date
        context["next_month"] = current_date.replace(day=1) + timedelta(days=32)

        return context

    def get_queryset(self):
        queryset = (
            Mood.objects.filter(user=self.request.user)
            .prefetch_related("activities")
            .only("mood", "note_title", "date", "time", "activities")
        )
        date = self.request.GET.get("date")
        if date is None:
            return queryset
        else:
            try:
                date = datetime.strptime(date, "%Y-%m").date()
                queryset = queryset.filter(
                    date__year=date.year,
                    date__month=date.month,
                )
            except ValueError:
                pass

        return queryset


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

    # def get_queryset(self):
    #     mood = self.request.GET.get("mood", "")
    #     search_term = self.request.GET.get("search_term", "")
    #     start_date = self.request.GET.get("start_date", "")
    #     end_date = self.request.GET.get("end_date", "")
    #
    #     moods = Mood.objects.filter(user=self.request.user)
    #
    #     if mood:
    #         moods = moods.filter(mood=mood)
    #     if search_term:
    #         moods = moods.filter(search_vector=search_term)
    #     if start_date:
    #         start_date = make_aware(datetime.strptime(start_date, "%Y-%m-%d"))
    #         moods = moods.filter(date__gte=start_date - timedelta(days=1))
    #     if end_date:
    #         end_date = make_aware(datetime.strptime(end_date, "%Y-%m-%d"))
    #         moods = moods.filter(date__lte=end_date + timedelta(days=1))
    #
    #     moods = moods.prefetch_related("activities")
    #     return moods
    #


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


class ImportView(LoginRequiredMixin, FormView):
    form_class = UploadFileForm
    template_name = "moods/import.html"
    success_url = reverse_lazy("mood_list")
    max_upload_size = settings.FILE_UPLOAD_MAX_MEMORY_SIZE

    def post(self, request, *args, **kwargs):
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            return self.handle_upload_file(form)
        else:
            form = UploadFileForm()
            return self.form_invalid(form)

    def handle_upload_file(self, form):
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
                date=timezone.datetime.strptime(row["date"], "%Y-%m-%d").date(),
                time=timezone.datetime.strptime(row["time"], "%H:%M:%S").time(),
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
                    date=timezone.datetime.strptime(item["date"], "%Y-%m-%d").date(),
                    time=timezone.datetime.strptime(item["time"], "%H:%M:%S").time(),
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
    template_name = "moods/export.html"
    success_url = reverse_lazy("mood_list")

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.create_export(form.cleaned_data["export_format"])

        return self.form_invalid(form)

    def create_export(self, export_format):
        moods = Mood.objects.filter(user=self.request.user).prefetch_related(
            "activities"
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
                "date": mood.date.strftime("%Y-%m-%d"),
                "time": mood.time.strftime("%H:%M:%S"),
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
        writer.writerow(["mood", "note_title", "note", "activities", "date", "time"])
        for mood in moods:
            writer.writerow(
                [
                    mood.mood,
                    mood.note_title,
                    mood.note,
                    ", ".join([activity.name for activity in mood.activities.all()]),
                    mood.date.strftime("%Y-%m-%d"),
                    mood.time.strftime("%H:%M:%S"),
                ]
            )
        return response
