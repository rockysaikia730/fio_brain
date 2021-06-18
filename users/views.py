from rest_framework.response import Response
from rest_framework.views import APIView
from . import serializers as ser


class UserView(APIView):

    def post(self, request):
        serializer = ser.UserSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.save())
        return Response(serializer.errors)


class PasswordResetView(APIView):

    def get(self, request):
        serializer = ser.PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.save())
        return Response(serializer.errors)
