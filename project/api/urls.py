from django.urls import path

from . import views

urlpatterns = [
    path("", views.event_handler, name="event_handler"),
    path("get_patterns/", views.get_patterns, name="get_patterns"),
    path("update_leaked_message/", views.update_leaked_message, name="update_leaked_message"),
]
