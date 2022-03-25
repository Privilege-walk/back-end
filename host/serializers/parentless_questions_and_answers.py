from rest_framework.serializers import ModelSerializer

from host.models import Question, AnswerChoice


class ParentlessAnswerSerializer(ModelSerializer):
    class Meta:
        model = AnswerChoice
        fields = (
            "id",
            "description",
            "value",
        )
