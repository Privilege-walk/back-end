from django.urls import path

from .controllers.event_apis import AllEvents

urlpatterns = [
    path('events/all/', AllEvents.as_view(), name="getAllEvents"),
]