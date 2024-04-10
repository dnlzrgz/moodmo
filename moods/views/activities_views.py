from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)
from utils.mixins import UserIsOwnerMixin, SetUserMixin
from moods.forms import ActivityForm
from moods.models import Activity


class ActivityListView(LoginRequiredMixin, ListView):
    model = Activity
    template_name = "moods/activity_list.html"
    context_object_name = "activities"
    ordering = ["name"]

    def get_queryset(self):
        return Activity.objects.filter(user=self.request.user).only("name", "sqid")


class ActivityCreateView(LoginRequiredMixin, SetUserMixin, CreateView):
    model = Activity
    form_class = ActivityForm
    template_name = "moods/activity_create.html"
    success_url = reverse_lazy("activity_list")


class ActivityUpdateView(
    LoginRequiredMixin, UserIsOwnerMixin, SetUserMixin, UpdateView
):
    model = Activity
    form_class = ActivityForm
    template_name = "moods/activity_update.html"
    success_url = reverse_lazy("activity_list")
    slug_field = "sqid"


class ActivityDeleteView(LoginRequiredMixin, UserIsOwnerMixin, DeleteView):
    model = Activity
    template_name = "moods/activity_delete.html"
    success_url = reverse_lazy("activity_list")
    context_object_name = "activity"
    slug_field = "sqid"
