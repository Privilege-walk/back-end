from django.contrib.auth.models import User
from django.db.utils import IntegrityError

from django.contrib import auth
from rest_framework.authtoken.models import Token

from rest_framework.permissions import AllowAny

from rest_framework.views import APIView
from rest_framework.response import Response


class SignUp(APIView):

    permission_classes = [AllowAny]

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


class Login(APIView):

    permission_classes = [AllowAny]

    def post(self, request, format=None):
        data = request.data

        username = data['username']
        password = data['password']

        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                auth.login(request, user)
                token, _ = Token.objects.get_or_create(user=user)
                return Response(
                    {
                        "status": True,
                        "token": token.key
                    }
                )

            else:
                return Response(
                    {
                        "status": False
                    }
                )

        except:
            return Response(
                {
                    "status": False
                }
            )