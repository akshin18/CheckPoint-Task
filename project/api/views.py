from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.http import JsonResponse

from api import handler


@api_view(["POST"])
def event_handler(request) -> Response:
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
            if not text:
                return Response(
                    {"detail": "'text' is required in the message."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            message_created = handler.save_message(text, client_msg_id)
            if message_created:
                return handler.add_event_to_redis(data)
            return Response(
                {"detail": "Message already exists."},
                status=status.HTTP_200_OK,
            )

    elif data_type == "url_verification":
        return Response(data, status=status.HTTP_200_OK)
    # Return a bad request if 'type' is not 'event_callback'
    return Response(
        {"detail": "'type' must be 'event_callback'."},
        status=status.HTTP_400_BAD_REQUEST,
    )


@api_view(["GET"])
def get_patterns(request) -> Response:
    # Get patterns from the handler
    return handler.get_patterns()


@api_view(["POST"])
def update_message(request) -> Response:
    # Extract the incoming data
    data = request.data
    client_msg_id = data.get("client_msg_id")
    pattern_id = data.get("pattern_id")
    return handler.update_message(client_msg_id, pattern_id)


def ping(request) -> JsonResponse:
    return JsonResponse({"status": "ok"})
