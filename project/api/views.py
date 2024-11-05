import re
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .handler import dlp


@api_view(["POST"])
def event_handler(request):
    # Extract the incoming data
    data = request.data

    # Check if 'type' is in the request data
    data_type = data.get("type")
    if not data_type:
        return Response(
            {"detail": "'type' field is required."}, status=status.HTTP_400_BAD_REQUEST
        )

    # Handle 'event_callback' type
    if data_type == "event_callback":
        event = data.get("event")

        # Ensure 'event' field is present
        if not event:
            return Response(
                {"detail": "'event' field is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Extract event type
        event_type = event.get("type")

        if event_type == "message":
            text = event.get("text", "")
            client_msg_id = event.get("client_msg_id")

            # Check for required message fields
            if not client_msg_id:
                return Response(
                    {"detail": "'client_msg_id' is required in the message."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Process the message with dlp handler
            dlp(text, client_msg_id)
            return Response({"detail": "Message processed."}, status=status.HTTP_200_OK)

    # Return a bad request if 'type' is not 'event_callback'
    return Response(
        {"detail": "'type' must be 'event_callback'."},
        status=status.HTTP_400_BAD_REQUEST,
    )
