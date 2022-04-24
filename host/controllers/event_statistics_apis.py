from pickle import TRUE
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.permissions import AllowAny

from host.models import Event
from user_mgmt.models import AnonymousParticipant
from host.utils.get_bars_stats import get_bars_statistics
from host.utils.get_participant_location import get_participant_location


class EventStatistics(APIView):
    # select position, count(position) as count from (select R.participant, sum(A.value) as position from Question Q, 
    # AnswerChoice A, Response R where Q.event = event_id and A.question_id = Q.question_id and R.answer_id = A.answer_id group by R.participant)
    permission_classes = [AllowAny]
    def get(self, request):
        print(request.query_params)
        event_id = request.query_params.get('event_id', None)
        print(event_id)
        participant_unique_code = request.query_params.get('unique_code', None)
        if event_id is None:
            return Response(
                {
                    "message": "Please enter an event ID"
                },
                status=500
            )

        try:
            event_in_focus = Event.objects.get(id=event_id)
            print(event_in_focus)

        except:
            return Response(
                {
                    "message": "The event ID that you've entered is not in the records"
                },
                status=400
            )
        position_stats = get_bars_statistics(event_id)
        results = {}
        results['barDefaultColor'] = '#8884d8'
        data = []
        participant_location = None
        if participant_unique_code is not None:
            try:
                participant = AnonymousParticipant.objects.get(unique_code = participant_unique_code)
            except:
                return Response(
                    {
                        "message": "The participant unique code that you've entered is not in the records"
                    },
                    status=400
                )
            participant_location = get_participant_location(event_id, participant_unique_code)
        results['x_label_min'] = event_in_focus.x_label_min
        results['x_label_max'] = event_in_focus.x_label_max
        for position in position_stats:
            line_data = {}
            line_data['barName'] = ''
            line_data['line_number'] = position['line_number']
            line_data['count'] = position['count']
            if participant_location is not None and position['line_number'] == participant_location['position']:
                line_data['participantLocation'] = True
            else:
                line_data['participantLocation'] = False
            data.append(line_data)

        results['data'] = data

        return Response(results)
