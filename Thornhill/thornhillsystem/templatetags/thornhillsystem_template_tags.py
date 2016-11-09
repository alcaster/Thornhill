import ntpath

from django import template

register = template.Library()


@register.filter()
def path_leaf(path):
    path = str(path)
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)
