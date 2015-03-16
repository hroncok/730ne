from django.contrib.auth.models import User
from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

from fitauth import get_roles


register = template.Library()


@register.filter(is_safe=True)
def detail(user):
    if user.get_full_name():
        output = '%s (%s)' % (user.get_full_name(), user.username)
    else:
        output = user.username

    roles = get_roles(user)
    if 'B-18000-ZAMESTNANEC' in roles:
        output += ' <span class="label label-info">zaměstnanec</span>'
    if 'B-18000-STUDENT' in roles:
        output += ' <span class="label label-primary">student</span>'
    if 'B-18000-UCASTNIK-CZV' in roles:
        output += ' <span class="label label-default">cžv</span>'

    return mark_safe(output)
