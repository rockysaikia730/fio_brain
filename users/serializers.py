from rest_framework import serializers
from .models import User
from .auth_token_builder import BuildLoginToken, BuildPasswordResetToken


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        instance = User.objects.create_user(**validated_data)
        return BuildLoginToken.build_token(instance)


class PasswordResetSerializer(serializers.Serializer):
    query = serializers.CharField(required=False)
    otp = serializers.CharField(required=False)

    def create(self, validated_data):
        user = User.objects.get_user_or_404(**validated_data)
        token = BuildPasswordResetToken.build_token(user)
        # This token will be sent to user via email/phone
        return token
