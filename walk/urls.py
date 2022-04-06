from django.urls import path

from .controllers import \
    qa_control_ws_consumer, \
    participant_registration

websocket_urlpatterns = [
    path('qa_control/<int:eventid>/', qa_control_ws_consumer.QAControlConsumer.as_asgi()),
]

urlpatterns = [
    path('register_participant/', participant_registration.ParticipantRegistration.as_view()),
]