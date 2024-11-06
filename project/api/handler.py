import json
import time
from typing import Optional

from rest_framework.response import Response
from redis import Redis

from .models import Pattern, FlaggedMessage
from .serializers import PatternSerializer

from project.settings import QUEUE_NAME, REDIS_HOST, REDIS_PORT, REDIS_DB


redis_client = Redis(REDIS_HOST, REDIS_PORT, REDIS_DB)


def get_patterns() -> Response:
    patterns = Pattern.objects.all()
    serializer = PatternSerializer(patterns, many=True)
    return Response(serializer.data)


def add_event_to_redis(data: dict) -> Response:
    # Add the event to the Redis sorted set
    raw_data = json.dumps(data, separators=(",", ":"))
    now = time.time()
    result = redis_client.zadd(QUEUE_NAME, {raw_data: now})
    if result:
        return Response({"detail": "Event added to Redis."}, status=200)
    return Response({"detail": "Failed to add event to Redis."}, status=500)


def save_message(text: str, client_msg_id: str) -> bool:
    # Extract the message data
    _, created = FlaggedMessage.objects.get_or_create(
        content=text, client_msg_id=client_msg_id
    )
    if created:
        return True
    return False


def update_message(client_msg_id: str, pattern_id: Optional[str]) -> Response:
    # Upload the leaked message to the API
    message = FlaggedMessage.objects.get(client_msg_id=client_msg_id)
    message.is_checked = True
    if pattern_id:
        message.matched_pattern = Pattern.objects.get(id=pattern_id)
    message.save()
    return Response({"detail": "Message updated."}, status=200)
