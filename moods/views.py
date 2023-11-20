from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from moods.forms import MoodForm
from .models import Mood


class MoodListView(ListView):
    model = Mood
    template_name = "moods/mood_list.html"
    context_object_name = "moods"


class MoodDetailView(DetailView):
    model = Mood
    template_name = "moods/mood_detail.html"
    context_object_name = "mood"


class MoodCreateView(CreateView):
    model = Mood
    form_class = MoodForm
    template_name = "moods/mood_form.html"
    success_url = reverse_lazy("mood_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class MoodUpdateView(UpdateView):
    model = Mood
    form_class = MoodForm
    template_name = "moods/mood_form.html"
    context_object_name = "mood"
    success_url = reverse_lazy("mood_list")


class MoodDeleteView(DeleteView):
    model = Mood
    template_name = "moods/mood_delete.html"
    success_url = reverse_lazy("mood_list")
    context_object_name = "mood"
