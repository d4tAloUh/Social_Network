from rest_framework import serializers
from ..models import Reaction


class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = '__all__'

    def create(self, validated_data):
        if validated_data['user'] != self.context['request'].user:
            raise serializers.ValidationError('You cannot create reaction for someone else')
        instance, created = Reaction.objects.get_or_create(**validated_data)

        if not created:
            instance.is_like = not instance.is_like
            instance.save(update_fields=['is_like'])
        return instance
