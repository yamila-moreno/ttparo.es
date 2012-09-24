# -*- coding: utf-8 -*-


from django import template
from django.contrib import messages
from django.utils.safestring import mark_safe

register = template.Library()

@register.inclusion_tag('menu.html', takes_context=True)
def main_menu(context):
    ctx = {
        'menu':context['menu'],
    }
    return ctx
