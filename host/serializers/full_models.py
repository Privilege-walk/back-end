from rest_framework.serializers import ModelSerializer

from host.models import Event


class FullEventSerializer(ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'