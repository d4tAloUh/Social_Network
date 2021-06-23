from rest_framework import serializers
from ..models import CustomUser


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'date_joined']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'id',
            'password',
            'email',
        )
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user
