from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)
from utils.mixins import UserIsOwnerMixin, SetUserMixin
from activities.models import Activity
from activities.forms import ActivityForm


class ActivityListView(LoginRequiredMixin, ListView):
    model = Activity
    template_name = "activities/activity_list.html"
    context_object_name = "activities"
    ordering = ["name"]

    def get_queryset(self):
        return Activity.objects.filter(user=self.request.user)


class ActivityCreateView(LoginRequiredMixin, SetUserMixin, CreateView):
    model = Activity
    form_class = ActivityForm
    template_name = "activities/activity_create.html"
    success_url = reverse_lazy("activity_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        if Activity.objects.filter(
            name=form.instance.name,
            user=self.request.user,
        ).exists():
            form.add_error("name", "An activity with this name already exists.")
            return self.form_invalid(form)

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
