from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated

from host.models import Event
from host.serializers import hostless


class AllEvents(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        host = request.user

        events_ser = hostless.HostlessEventSerializer(Event.objects.filter(host=host), many=True)
        return Response(
            {
                "events": events_ser.data
            }
        )


class CreateEvent(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        event = Event.objects.create(
            host=request.user,
            name=request.data["name"],
            status="created",
        )

        return Response(
            {
                "status": event.status,
                "id": event.id,
            }
        )