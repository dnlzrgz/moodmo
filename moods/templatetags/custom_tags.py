from datetime import timedelta
from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def next_month(context, format_str="%Y-%m"):
    date = context.get("current_month")
    next_month_date = date.replace(day=1) + timedelta(days=32)
    return next_month_date.strftime(format_str)


@register.simple_tag(takes_context=True)
def prev_month(context, format_str="%Y-%m"):
    date = context.get("current_month")
    prev_month_date = date.replace(day=1) - timedelta(days=1)
    return prev_month_date.strftime(format_str)
