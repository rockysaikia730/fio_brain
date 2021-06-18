from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .utils import set_lifetime


class BuildLoginToken(TokenObtainPairSerializer):

    @classmethod
    def build_token(cls, user):
        token = super().get_token(user)
        token['user_type'] = user.user_type
        return {
            'access_token': str(token.access_token),
            'refresh_token': str(token)
        }


class BuildPasswordResetToken(TokenObtainPairSerializer):
    @classmethod
    def build_token(cls, user):
        token = super().get_token(user)
        token['token_type'] = 'password_reset'
        token['user_type'] = user.user_type
        # cup -> current user password
        # cup will help us to identify used token
        token['exp'] = set_lifetime(minutes=5)
        token['cup'] = user.password
        return str(token)
