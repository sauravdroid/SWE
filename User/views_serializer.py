from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser
from .Serializers import CustomUserSerializer


class CustomUserList(APIView):
    def get(self, request):
        custom_user = CustomUser.objects.all()
        serializer = CustomUserSerializer(custom_user, many=True)
        return Response(serializer.data)

    def post(self):
        pass
