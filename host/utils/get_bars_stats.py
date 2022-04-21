from django.db.models import Sum

from host.models import Question, AnswerChoice, Event
from walk.models import Response


def get_bars_statistics(event_id):
    event_in_focus = Event.objects.get(id=event_id)
    event_questions = Question.objects.filter(event=event_in_focus)
    choices = AnswerChoice.objects.filter(question__in = event_questions)
    positions = Response.objects.filter(answer__in = choices).values('participant').annotate(position=Sum('answer__value')).order_by('position')
    distinct_positions = positions.values('position').distinct()
    position_stats = []

    for position in distinct_positions:
        pos = position['position']
        count = positions.filter(position = pos).count()
        line_stats = {}
        line_stats['line_number'] = pos
        line_stats['count'] = count
        position_stats.append(line_stats)

    return position_stats



        