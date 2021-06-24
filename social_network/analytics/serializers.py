from rest_framework import serializers
from api.models import Reaction


class TestSerializer(serializers.ModelSerializer):
    amount = serializers.IntegerField(min_value=0, default=0)

    class Meta:
        model = Reaction
        fields = ['created_at', 'id', 'amount']
