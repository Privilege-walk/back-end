from django.db.models import Sum

from host.models import Question, AnswerChoice, Event
from walk.models import Response


def get_question_response_statistics(event_id):
    event_in_focus = Event.objects.get(id=event_id)
    event_questions = Question.objects.filter(event=event_in_focus)
    response_stats = []
    for question in event_questions:
        question_stats = {}
        question_stats['question_id'] = question.id
        question_stats['question'] = question.description
        choices = AnswerChoice.objects.filter(question = question)
        answers = []
        for choice in choices:
            answer = {}
            answer['answer_id'] = choice.id
            answer['answer'] = choice.description
            count = Response.objects.filter(answer = choice).count()
            answer['count'] = count
            answers.append(answer)
        question_stats['answers'] = answers
        response_stats.append(question_stats)
    
    return response_stats
