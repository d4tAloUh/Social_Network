from datetime import datetime

from rest_framework import serializers
from ..models import Post, Reaction


class PostSerializer(serializers.ModelSerializer):
    likes_amount = serializers.SerializerMethodField()
    dislikes_amount = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'

    def get_likes_amount(self, instance):
        return Reaction.objects.filter(post=instance, is_like=True).count()

    def get_dislikes_amount(self, instance):
        return Reaction.objects.filter(post=instance, is_like=False).count()

    def create(self, validated_data):
        if validated_data['user'] != self.context['request'].user:
            raise serializers.ValidationError('You cannot create post for someone else')
        return super(PostSerializer, self).create(validated_data)

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['created_at'] = datetime.fromtimestamp(instance.created_at.timestamp()).strftime('%Y-%m-%d %H:%M:%S')
        return rep
