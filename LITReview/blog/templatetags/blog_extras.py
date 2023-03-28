from django.template import Library

register = Library()


@register.simple_tag(takes_context=True)
def get_poster_display(context, user):
    if context['user'] == user:
        return 'vous'
    return user.username


@register.simple_tag()
def get_stars(context):
    if context == 0:
        return '☆☆☆☆☆'
    elif context == 1:
        return '★☆☆☆☆'
    elif context == 2:
        return '★★☆☆☆'
    elif context == 3:
        return '★★☆☆'
    elif context == 4:
        return '★★★★☆'
    elif context == 5:
        return '★★★★★'
