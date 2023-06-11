from django import template

register = template.Library()

@register.filter
def total_seconds(duration):
    return int(duration.total_seconds())
