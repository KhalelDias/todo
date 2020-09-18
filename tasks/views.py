from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class TestResponseView(APIView):

    def get(self, request):
        permission_classes = [IsAuthenticated]
        return Response({'one': 'knocks'})
