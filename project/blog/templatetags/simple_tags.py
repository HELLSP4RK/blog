import random

from django import template


register = template.Library()


@register.simple_tag
def random_color():
    colors = [
        'violet',
        'purple',
        'blue',
        'cyan',
        'green',
        'orange',
        'red',
    ]
    return random.choice(colors)
