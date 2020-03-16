from django import template

register = template.Library()

@register.filter()
def maxlength(iterable, length):
    return iterable[:min(len(iterable), length)]
