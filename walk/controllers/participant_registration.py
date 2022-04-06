from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.permissions import AllowAny


from user_mgmt.models import AnonymousParticipant
from host.models import Event

class ParticipantRegistration(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        inData = request.data

        try:
            event_in_focus = Event.objects.get(id=inData["event_id"])
        except:
            return Response(
                {
                    "message": "Event not found, try a different event ID"
                },
                status=400
            )

        anno_user = AnonymousParticipant.objects.create(
            event=event_in_focus
        )
        anno_user.save()

        return Response(
            {
                "status": "registered",
                "participant_code": anno_user.unique_code
            }
        )