from django import template
from django.utils.safestring import mark_safe
import mistune

@register.filter(is_safe=True)
def markdown(value):
    """
    Runs Markdown on a given value

    Syntax::

        {{ value|markdown }}

    """
    import mistune

    return mark_safe(mistune.markdown(force_text(value)))
