from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Custom template filter to access dictionary values dynamically"""
    return dictionary.get(key, "")
