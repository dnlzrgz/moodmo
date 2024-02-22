from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)
from moods.mixins import UserIsOwnerMixin, SetUserMixin
from activities.models import Activity
from activities.forms import ActivityForm


class ActivityListView(LoginRequiredMixin, ListView):
    model = Activity
    template_name = "activities/activity_list.html"
    context_object_name = "activities"
    ordering = ["name"]


class ActivityCreateView(LoginRequiredMixin, SetUserMixin, CreateView):
    model = Activity
    form_class = ActivityForm
    template_name = "activities/activity_create.html"
    success_url = reverse_lazy("activity_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ActivityUpdateView(
    LoginRequiredMixin, UserIsOwnerMixin, SetUserMixin, UpdateView
):
    model = Activity
    form_class = ActivityForm
    template_name = "activities/activity_update.html"
    success_url = reverse_lazy("activity_list")
    slug_field = "sqid"


class ActivityDeleteView(LoginRequiredMixin, UserIsOwnerMixin, DeleteView):
    model = Activity
    template_name = "activities/activity_delete.html"
    success_url = reverse_lazy("activity_list")
    context_object_name = "activity"
    slug_field = "sqid"
