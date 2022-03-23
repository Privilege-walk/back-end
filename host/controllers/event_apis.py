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