from django.urls import path

from .controllers.event_apis import AllEvents, CreateEvent
from .controllers.question_answer_apis import AddQuestion

urlpatterns = [
    path('events/all/', AllEvents.as_view(), name="getAllEvents"),
    path('events/create/', CreateEvent.as_view(), name="createNewEvent"),
    path('qa/create/', AddQuestion.as_view(), name="addQuestion"),
]