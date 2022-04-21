from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated

from host.models import Event
from host.utils.get_question_response_stats import get_question_response_statistics


class QuestionResponseStatistics(APIView):
    # select position, count(position) as count from (select R.participant, sum(A.value) as position from Question Q, 
    # AnswerChoice A, Response R where Q.event = event_id and A.question_id = Q.question_id and R.answer_id = A.answer_id group by R.participant)
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        print(request.query_params)
        event_id = request.query_params.get('event_id', None)

        if event_id is None:
            return Response(
                {
                    "message": "Please enter an event ID"
                },
                status=500
            )

        try:
            event_in_focus = Event.objects.get(id=event_id)

        except:
            return Response(
                {
                    "message": "The event ID that you've entered is not in the records"
                },
                status=400
            )

        question_response_stats = get_question_response_statistics(event_id)

        return Response(question_response_stats)
