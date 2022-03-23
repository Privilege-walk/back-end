from rest_framework.serializers import ModelSerializer

from host.models import Event


class HostlessEventSerializer(ModelSerializer):
    class Meta:
        model = Event
        fields = [
            'id', 'name', 'status',
        ]