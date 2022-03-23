from django.test import TestCase

from django.contrib.auth.models import User
from host.models import Event, Question, AnswerChoice


class TestQuestionAnswer(TestCase):
    def setUp(self) -> None:
        event_host = User.objects.create_user(
            username="acoolsomebody",
            password="somethigcool",
            email="acoolsomebody@email.com"
        )

        self.event = Event.objects.create(
            host=event_host,
            name="Rodeo",
            status="created",
        )

    def test_question_answers(self):
        q1 = Question.objects.create(
            event=self.event,
            description="This is the 1st question"
        )

        AnswerChoice.objects.create(
            question=q1,
            description="Pizza",
            value=1
        )

        AnswerChoice.objects.create(
            question=q1,
            description="Ice Cream",
            value=-2
        )

        self.assertEqual(
            Question.objects.all()[0].description,
            "This is the 1st question",
        )

        answer_choices = AnswerChoice.objects.filter(question__description="This is the 1st question")
        self.assertEqual(len(answer_choices), 2)

        second_choice = answer_choices[1]

        self.assertEqual(
            second_choice.value,
            -2
        )
