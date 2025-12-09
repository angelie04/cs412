from django.shortcuts import render
from django.views.generic import *
from project.models import *
from django.shortcuts import redirect, render, get_object_or_404
from .forms import *
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm ## for new User
from django.urls import reverse
import random
from django.db.models import Q, Avg, Count
from django.forms import inlineformset_factory # for formsets
from django.db import transaction




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

    def get_queryset(self):
        # annotate with average rating (uses related_name 'reviews' on Review FK)
        qs = Restaurant.objects.all().annotate(avg_rating=Avg('reviews__rating'), reviews_count=Count("reviews"))
        sort = self.request.GET.get("sort", "").strip()

        if sort == "rating_desc":
            qs = qs.order_by("-avg_rating", "-name")
        elif sort == "rating_asc":
            qs = qs.order_by("avg_rating", "name")
        elif sort == "name_desc":
            qs = qs.order_by("-name")
        elif sort == "name_asc":
            qs = qs.order_by("name")
        # default ordering can be set here if desired
        return qs

class ReviewView(TemplateView):
    """View to render the review page."""
    
    model = Review
    template_name = "project/review.html"
    
class WriteReview(CreateView):
    """View to create a review for a restaurant."""
    
    model = Review
    form_class = ReviewForm
    template_name = "project/write_review.html"

    # inline formset factory for review images
    ReviewImageFormSet = inlineformset_factory(
        Review, Review_images, fields=("image",), extra=3, max_num=5, can_delete=False
    )

    def dispatch(self, request, *args, **kwargs):
        # ensure restaurant exists before showing form
        self.restaurant = Restaurant.objects.filter(pk=self.kwargs.get("restaurant_id")).first()
        if not self.restaurant:
            return render(request, "project/404.html", status=404)
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.restaurant = self.restaurant
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if "formset" in kwargs:
            ctx["formset"] = kwargs["formset"]
        else:
            ctx["formset"] = self.ReviewImageFormSet(instance=Review())
        ctx["restaurant"] = self.restaurant
        return ctx
    
    def post(self, request, *args, **kwargs):
        """This does the form + formset submission."""
        form = self.get_form()
        formset = self.ReviewImageFormSet(request.POST, request.FILES, instance=Review())
        if form.is_valid() and formset.is_valid():
            return self.form_valid_with_formset(form, formset)
        return self.form_invalid_with_formset(form, formset)
    
    def form_valid_with_formset(self, form, formset):
        # Save review then images atomically
        with transaction.atomic():
            review = form.save(commit=False)
            # attach user if available
            if self.request.user.is_authenticated:
                review.user = self.request.user
            review.restaurant = self.restaurant
            review.save()
            # bind formset to saved review and save images
            self.object = review
            formset.instance = review
            formset.save()
        return redirect(self.get_success_url())

    def form_invalid_with_formset(self, form, formset):
        # render template with bound formset and form errors
        context = self.get_context_data(form=form, formset=formset)
        return self.render_to_response(context)
    
    def get_success_url(self):
        return reverse('success_review')
    
class ReviewSuccessView(TemplateView):
    """View for review submission success page."""
    
    template_name = "project/success_review.html"
    
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
    
class RestaurantDetailView(DetailView):
    """View to display details of a single Restaurant"""
    model = Restaurant
    template_name = "project/restaurant_detail.html"
    context_object_name = "restaurant"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # add reviews related to this restaurant
        context['reviews'] = Review.objects.filter(restaurant=self.object)
        context["map_query"] = self.object.address
        # finding average rating and review count
        agg = context['reviews'].aggregate(avg=Avg('rating'), count=Count('pk'))
        context['avg_rating'] = agg['avg']            
        context['reviews_count'] = agg['count'] or 0
        return context
