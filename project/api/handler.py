import re

from .models import Pattern, FlaggedMessage


def dlp(text: str, client_msg_id: str) -> None:
    patterns = Pattern.objects.all()
    for pattern in patterns:
        if re.search(pattern.regex, text):
            FlaggedMessage.objects.get_or_create(
                content=text, matched_pattern=pattern, client_msg_id=client_msg_id
            )
