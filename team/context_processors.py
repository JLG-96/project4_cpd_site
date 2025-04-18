from .models import Notification


def notification_context(request):
    if request.user.is_authenticated:
        unread = Notification.objects.filter(
            recipient=request.user, is_read=False).exists()
        return {'new_notifications': unread}
    return {}
