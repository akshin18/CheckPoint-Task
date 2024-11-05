from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from .models import Pattern, FlaggedMessage


@api_view(["POST"])
async def event_handler(request):
    data = request.data
    data_type = data.get("event_type")
    if not data_type:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    if data_type == "event_callback":
        event = data.get("event")
        event_type = event.get("type")
        if event_type == "message":
            text = event.get("text")

        return Response(status=status.HTTP_400_BAD_REQUEST)
