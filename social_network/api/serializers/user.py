from datetime import datetime

from rest_framework import serializers
from ..models import CustomUser


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'date_joined', 'last_activity']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['last_activity'] = datetime.fromtimestamp(instance.last_activity.timestamp()).strftime('%Y-%m-%d %H:%M:%S')
        rep['date_joined'] = datetime.fromtimestamp(instance.date_joined.timestamp()).strftime('%Y-%m-%d %H:%M:%S')
        return rep

class UserRegistrationSerializer(serializers.ModelSerializer):
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
