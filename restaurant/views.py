# File: restaurant/views.py
# Author: Angelie Darbouze (angelie@bu.edu)
# view functions to handle URL requests
from django.shortcuts import render, redirect
from django.http import HttpResponse
from datetime import datetime, timedelta
from django.utils import timezone
import random

#global scope
TODAYS_SPECIAL =[
    "Dreaming Princess cake slice $9.50",
    "Banana Nutella Cake slice $9.50",
    "Hostess Ding Dong Cake slice $9.50",
]
# Menu with prices
MENU = {
    "Brooklyn Blackout Cupcake $5": 5.00,
    "Red Velvet Cupcake $5": 5.00,
    "Golden Vanilla Cupcake $5": 5.00,
    "Carrot Cupcake $5": 5.00,
    "Golden Chocolate Cupcake $5": 5.00,
    "Milk $2.50": 2.50,
    "Dreaming Princess cake slice $9.50": 9.50,
    "Banana Nutella Cake slice $9.50": 9.50,
    "Hostess Ding Dong Cake slice $9.50": 9.50,
}
# Create your views here.
def home (request):
    """ Show the home page for the restaurant """
    
    template_name = "restaurant/home.html"
    image = ""
    return render(request, template_name, {"image": image})
def order_form(request):
    """ Show the form to the user """
    template_name = "restaurant/form.html"
    special = random.choice(TODAYS_SPECIAL)
    context = {
        'special': special,
    }
    return render(request, template_name, context)

def submit(request):
    """ Process the form submission """
    template_name = "restaurant/confirmation.html"

    if request.POST:
        # Get all cupcake selections from the form
        cupcakes = request.POST.getlist("cupcake")
        # Get special instructions and contact info
        instructions = request.POST.get("instructions", "")
        name = request.POST.get("name")
        phone = request.POST.get("phone", "")
        email = request.POST.get("email", "")
         # Calculate total
        total = float(sum(MENU.get(item.strip(), 0) for item in cupcakes))
        # Generates a random ready time (30-60 minutes from now US time)
        minutes = random.randint(30, 60)
        ready_time = timezone.localtime() + timedelta(minutes=minutes)
        ready_time_str = ready_time.strftime("%I:%M %p")
        context = {
            "name": name,
            "phone": phone, 
            "email": email,
            "cupcakes": cupcakes,
            "instructions": instructions,
            "ready_time": ready_time_str,
            "total": total,
        }
        return render(request, template_name= template_name, context=context)
    else:
        return redirect("order_form")