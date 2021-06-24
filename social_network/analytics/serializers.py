from datetime import datetime

from rest_framework import serializers
from api.models import Reaction


class TestSerializer(serializers.ModelSerializer):
    amount = serializers.IntegerField(min_value=0, default=0)

    class Meta:
        model = Reaction
        fields = ['created_at', 'id', 'amount']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['created_at'] = datetime.fromtimestamp(instance.created_at.timestamp()).strftime('%Y-%m-%d %H:%M:%S')
        return rep
