from django.db.models import Sum

from host.models import Question, AnswerChoice, Event
from walk.models import Response
from user_mgmt.models import AnonymousParticipant


def get_participant_location(event_id, participant_unique_code):
    event_in_focus = Event.objects.get(id=event_id)
    event_questions = Question.objects.filter(event=event_in_focus)
    choices = AnswerChoice.objects.filter(question__in = event_questions)
    participant = AnonymousParticipant.objects.filter(unique_code = participant_unique_code)
    position_details = Response.objects.filter(answer__in = choices, participant__in = participant).values('participant').annotate(position=Sum('answer__value'))
    participant_details = {}
    participant_details['participant_id'] = position_details[0]['participant']
    participant_details['position'] = position_details[0]['position']
    return participant_details



        