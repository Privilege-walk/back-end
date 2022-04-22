from django.urls import path

from .controllers.event_apis import AllEvents, CreateEvent
from .controllers.question_answer_apis import AddQuestion, EventQuestionAnswers
from .controllers.question_response_stats_apis import QuestionResponseStatistics
from .controllers.event_statistics_apis import EventStatistics

urlpatterns = [
    path('events/all/', AllEvents.as_view(), name="getAllEvents"),
    path('events/create/', CreateEvent.as_view(), name="createNewEvent"),
    path('qa/create/', AddQuestion.as_view(), name="addQuestion"),
    path('qa/eventwise_qas/', EventQuestionAnswers.as_view(), name="fullEventDetails"),
    path('qa_stats/', QuestionResponseStatistics.as_view(), name="getQAStats"),
    path('event_stats/', EventStatistics.as_view(), name="eventStats")
]