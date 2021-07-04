from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed, NotFound
from . import serializers as ser
from .models import User
from .auth_token_builder import BuildLoginToken
from rest_framework_simplejwt.serializers import TokenVerifySerializer, TokenRefreshSerializer

        
class UserView(APIView):
    def post(self, request):
        serializer = ser.UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        tokens = serializer.save()
        response = Response(tokens['access_token'])
        response.set_cookie(key="jwt", value=str(tokens['refresh_token']), path='/', httponly=True)
        return response
        

class LoginView(APIView):
    def post(self, request):
        phone = request.data['phone']
        password = request.data['password']

        user = User.objects.filter(phone=phone).first()

        if user is None:
            raise AuthenticationFailed('User not Found')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect Password')

        tokens = BuildLoginToken.build_token(user) 
        response = Response(tokens['access_token'])
        response.set_cookie(key="jwt", value=str(tokens['refresh_token']), path='/', httponly=True)
        return response


class AccessView(APIView):
    def get(self, request):
        pass
        


class PasswordResetView(APIView):

    def get(self, request):
        serializer = ser.PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.save())
        return Response(serializer.errors)


class VerifyRefreshTokenView(APIView):
    #Validates the refresh token from the httponly cookie and returns new access token
    #otherwise generates error adn returns to signup page
    def get(self, request):
        try:
            token = request.COOKIES['jwt']
            data_response = TokenVerifySerializer().validate({'token': token})
            if not data_response:
                accesstoken = TokenRefreshSerializer().validate({'refresh': token})
                return Response({'access_token':accesstoken})
        except:
            raise NotFound('Not a valid token')
