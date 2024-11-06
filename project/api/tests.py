import pytest
from django.test import Client
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from api.models import Pattern, FlaggedMessage

client = APIClient()


@pytest.mark.django_db()
def test_event_handler_missing_type():
    url = reverse('event_handler')
    response = client.post(url, data={}, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['detail'] == "'type' field is required."


@pytest.mark.django_db()
def test_event_handler_event_callback_missing_event():
    url = reverse('event_handler')
    response = client.post(url, {"type": "event_callback"})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['detail'] == "'event' field is required."


@pytest.mark.django_db()
def test_event_handler_event_callback_message_missing_text():
    url = reverse('event_handler')
    response = client.post(url, {"type": "event_callback", "event": {"type": "message"}}, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_event_handler_url_verification():
    url = reverse('event_handler')
    data = {"type": "url_verification"}
    response = client.post(url, data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == data


@pytest.mark.django_db
def test_get_patterns():
    url = reverse('get_patterns')
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    # Add more assertions based on the expected response


@pytest.mark.django_db
def test_update_message():
    pattern = Pattern.objects.create(name="Parent", regex=".wqeqwe")
    FlaggedMessage.objects.create(client_msg_id="123", matched_pattern=pattern)
    url = reverse('update_message')
    data = {"client_msg_id": "123", "pattern_id": pattern.id}
    response = client.post(url, data)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_ping():
    client = Client()
    response = client.get(reverse('ping'))
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}