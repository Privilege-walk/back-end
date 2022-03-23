from django.urls import path

from .controllers.event_apis import AllEvents, CreateEvent

urlpatterns = [
    path('events/all/', AllEvents.as_view(), name="getAllEvents"),
    path('events/create/', CreateEvent.as_view(), name="createNewEvent"),
]