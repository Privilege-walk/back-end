from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated

from host.models import Question, AnswerChoice, Event
from host.serializers import hostless, parentless_questions_and_answers


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


class EventQuestionAnswers(APIView):
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

        # Initializing the output dictionary with the event details
        event_details = hostless.HostlessEventSerializer(event_in_focus).data

        # Iterating over the questions in the event
        event_questions = Question.objects.filter(event=event_in_focus)
        questions_list = []

        for question in event_questions:
            question_data = {
                "id": question.id,
                "description": question.description
            }

            choices = parentless_questions_and_answers.ParentlessAnswerSerializer(AnswerChoice.objects.filter(question=question).order_by('-value'), many=True).data
            question_data["choices"] = choices

            questions_list.append(question_data)

        event_details["questions"] = questions_list

        return Response(event_details)
