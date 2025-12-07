
from django import template
from project.models import Category

register = template.Library()

@register.inclusion_tag('project/category_dropdown.html', takes_context=True)
def category_dropdown(context):
    # returns all categories for the navbar dropdown
    cats = Category.objects.all()
    return {'categories': cats, 'request': context.get('request')}