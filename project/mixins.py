# project/mixins.py
# was created to hold custom mixins for the project app
#Angelie Darbouze (angelie@bu.edu), 12/9/2025
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from project.models import Profile

class ProfileLoginRequiredMixin(LoginRequiredMixin):
    """Custom mixin to require login and provide the current profile automatically."""
    login_url = 'login'  

    def get_login_url(self):
        return reverse(self.login_url)

    def get_logged_in_profile(self):
        user = getattr(self.request, "user", None)
        if not user or user.is_anonymous:
            return None
        # return first matching profile or None
        # return Profile.objects.filter(user=user).first()
        return Profile.objects.filter(revize_user=user).first()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.setdefault("profile", self.get_logged_in_profile())
        return ctx