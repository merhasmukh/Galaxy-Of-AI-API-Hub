from rest_framework.views import APIView
from rest_framework.response import Response

class RootView(APIView):
    def get(self, request):
        return Response({"message": "Welcome to the API!"})