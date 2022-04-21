from django.db.models import Sum, Count
from rest_framework.views import APIView

from rest_framework.permissions import IsAuthenticated

from host.models import Question, AnswerChoice, Event
from walk.models import Response
from host.utils import get_bars_stats


class EventStatistics(APIView):
    # select position, count(position) as count from (select R.participant, sum(A.value) as position from Question Q, 
    # AnswerChoice A, Response R where Q.event = event_id and A.question_id = Q.question_id and R.answer_id = A.answer_id group by R.participant)
    permission_classes = [IsAuthenticated]

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

        position_stats = get_bars_stats(event_id)
