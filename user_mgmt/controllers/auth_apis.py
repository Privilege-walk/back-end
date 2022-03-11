from django.contrib.auth.models import User
from django.db.utils import IntegrityError

from rest_framework.views import APIView
from rest_framework.response import Response

class SignUp(APIView):
    def post(self, request):
        in_data = request.data

        # Raising an error if email exists
        try:
            usr = User.objects.get(email=in_data["email"])
            return Response(
                {
                    "created": "email exists"
                }
            )
        except(User.DoesNotExist):
            pass

        # Creating the user if the username does not exist
        try:
            usr = User.objects.create_user(
                username=in_data["username"],
                password=in_data["password"],
                email=in_data["email"],
            )

        except(IntegrityError):
            return Response(
                {
                    "created": "username exists"
                }
            )

        usr.first_name = in_data["first_name"]
        usr.last_name = in_data["last_name"]
        usr.save()

        return Response(
            {
                "created": "success"
            }
        )