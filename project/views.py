from django.shortcuts import render
from django.views.generic import *
from project.models import *
from django.shortcuts import redirect
from .forms import *
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm ## for new User
from django.urls import reverse
import random
from django.db.models import Q


# Create your views here.

class HomeView(TemplateView):
    """View for the home page."""

    template_name = "project/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # show a few restaurants on the homepage 
        context["restaurants"] = Restaurant.objects.all()[:6]
        #randomly select 6 restaurants
        #Check to see if this works for your larger dataset
        ids = list(Restaurant.objects.values_list("id", flat=True))
        if not ids:
            context["restaurants"] = Restaurant.objects.none()
            return context
        random_ids = random.sample(ids, min(len(ids), 6))
        qs = Restaurant.objects.filter(id__in=random_ids)
        id_map = {r.id: r for r in qs}
        context["restaurants"] = [id_map[i] for i in random_ids if i in id_map]
        return context

class RestaurantListView(ListView):
    """View to list all restaurants."""
    
    model = Restaurant
    template_name = "project/restaurant_list.html"
    context_object_name = "restaurants"

class ReviewView(CreateView):
    """View to create a review for a restaurant."""
    
    model = Review
    form_class = ReviewForm
    template_name = "project/review.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.restaurant_id = self.kwargs['restaurant_id']
        return super().form_valid(form)

    def get_success_url(self):
        return redirect('restaurant_list')
    
class UserLogoutView(TemplateView):
    """View for logout confirmation page."""
    
    template_name = "project/logout.html"

class SignUpView(CreateView):
    """View to handle user sign up."""
    
    form_class = SignUpForm
    template_name = "project/signup.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        # Log the user in after successful sign up
        login(self.request, self.object)
        return redirect(self.get_success_url())
    def get_success_url(self):
        return reverse('home')  # Redirect to home page after sign up
    
class ProfileDetailView(DetailView):
    """View to display individual user profile details."""
    
    model = Profile
    template_name = "project/profile_detail.html"
    context_object_name = "profile"

class RestaurantSearchView(ListView):
    """View class to hanlde searching for restaurants """
    model = Restaurant
    template_name = "project/search_results.html"
    context_object_name = "restaurants"

    def dispatch(self, request, *args, **kwargs):
        """Override dispatch to check for the presence of the query parameter."""
        # if query is empty, redirect to search page
        if 'query' in request.GET and not request.GET.get('query', '').strip():
            return redirect('search_results')
        # If no query param present, render a simple search form
        if not request.GET.get("query"):
            return render(request, "project/search.html")
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        """Filter restaurants based on the search query."""

        query = self.request.GET.get("query", "").strip()
        if not query:
            return Restaurant.objects.none()
        qs = (
            Restaurant.objects.filter(
                Q(name__icontains=query)
                | Q(address__icontains=query)
                | Q(categories__name__icontains=query)
            )
            .distinct()
            .prefetch_related("categories")
        )
        return qs
    
    def get_context_data(self, **kwargs):
        """Add additional context data for the search results page."""

        ctx = super().get_context_data(**kwargs)
        ctx["query"] = self.request.GET.get("query", "")
        return ctx