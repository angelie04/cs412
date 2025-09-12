# File: views.py
# Author: Angelie Darbouze (angelie@bu.edu), 9/12/2025
# Description: Services each URL pattern, generates context data, and delegates presentation to the appropriate HTML template.

from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
import random
#Global scope
QUOTES = [
"I don't like being limited. This is my worst nightmare. I want to be able to flex other muscles and see what else I can do.",
"Food is my destination, my journey, my reward, my friend.",
"If a company is only as good as its weakest employee, then what does that say about you and the job you hold?",
"Don't misunderstand me; I don't want to die alone, but spending quality time with myself 60 to 70 percent of the day is my idea of mecca.",
]
IMAGES =[
    "https://hips.hearstapps.com/hmg-prod/images/elm110122wlrae-007a-1665427688.jpg?resize=980:*",
    "https://www.rollingstone.com/wp-content/uploads/2024/01/Issae-Rae-Black-representation.jpg?w=1581&h=1054&crop=1",
    "https://media.self.com/photos/614baef8f502073832591397/4:3/w_2240,c_limit/08.07.21_SELF_ISSARAE-3_Extended.png",
    "https://api.time.com/wp-content/uploads/2022/05/Issa-Rae-time100-2022.jpg?quality=85&w=1800",

]
def main_page(req):
    """ Creates the main page with random quotes and image. """
    template_name = 'quotes/main_page.html'
    quote = random.choice(QUOTES)
    image = random.choice(IMAGES)
    context = {
        'quote': quote,
        'image': image
    }
    return render(req,template_name, context)

def about_page(req):
    """ Creates the about page. """
    template_name = 'quotes/about.html'
    return render(req,template_name)

def show_all(req):
    """ Creates a page displaying all quotes and images. """
    template_name = 'quotes/show_all.html'
    context = {
        'quotes': QUOTES,
        'images': IMAGES
    }
    return render(req,template_name, context)