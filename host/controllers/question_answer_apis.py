from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated

from host.models import Question, AnswerChoice, Event


class AddQuestion(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        in_data = request.data

        question = Question.objects.create(
            event=Event.objects.get(id=in_data["event_id"]),
            description=in_data["title"]
        )

        for answer_choice in in_data["choices"]:
            AnswerChoice.objects.create(
                question=question,
                description=answer_choice["description"],
                value=answer_choice["value"],
            )

        return Response(
            {
                "status": "created",
                "id": question.id,
            }
        )