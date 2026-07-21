

from datetime import timedelta
from django.utils import timezone

from django.utils.timesince import timesince

def get_user_status(user):

    if not user.last_seen:
        return {
            "is_online": False,
            "status_text": "Offline"
        }

    is_online = (
        timezone.now() - user.last_seen
    ) <= timedelta(minutes=5)

    if is_online:
        status_text = "Online"
    else:
        status_text = f"Last seen {timesince(user.last_seen)} ago"

    return {
        "is_online": is_online,
        "status_text": status_text
    }