from django.urls import path

from .controllers import qa_control_ws_consumer

websocket_urlpatterns = [
    path('qa_control/<int:eventid>/', qa_control_ws_consumer.QAControlConsumer.as_asgi()),
]