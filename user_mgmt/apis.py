from rest_framework.views import APIView
from rest_framework.response import Response

class SayHello(APIView):
    def get(self, request, format = None):
        return Response(
            {
                "message": "Howdy! Thanks for visiting the back-end of Privilege Walk"
            }
        )