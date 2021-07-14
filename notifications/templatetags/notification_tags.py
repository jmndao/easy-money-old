from django import template

register = template.Library()


def user_context(context):
    if 'user' not in context:
        return None
    req = context['request']
    user = req.user
    
    return user

@register.simple_tag
def notification_count(context):
    user = user_context(context)
    if not user:
        return 0
    return user.notif_to.filter(read=False).count()

notification_count = register.simple_tag(takes_context=True)(notification_count)
