from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy


class UserIsOwnerMixin(UserPassesTestMixin):
    def test_func(self):
        return self.get_object().user == self.request.user

    def handle_no_permission(self):
        return HttpResponseRedirect(reverse_lazy("mood_list"))


class SetUserMixin:
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
