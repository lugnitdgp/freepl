from django import template
from datetime import date, timedelta

register = template.Library()

@register.filter(name='is_in')
def is_in(var, args):
    if args is None:
        return False
    arg_list = [arg.strip() for arg in args.split(',')]
    return var in arg_list

