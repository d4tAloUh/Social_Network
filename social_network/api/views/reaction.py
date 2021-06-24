from django.db import IntegrityError
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..models import Reaction
from ..serializers import ReactionSerializer


class ReactionListAPIView(generics.ListAPIView):
    queryset = Reaction.objects.all()
    serializer_class = ReactionSerializer
    permission_classes = [IsAuthenticated]


class ReactionListByPostAPIView(generics.ListAPIView, generics.CreateAPIView, generics.DestroyAPIView):
    serializer_class = ReactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Reaction.objects.filter(post_id=self.kwargs['post_id'])

    def get_object(self):
        return Reaction.objects.get(post_id=self.kwargs['post_id'], user=self.request.user)

    def perform_create(self, serializer):
        try:
            super(ReactionListByPostAPIView, self).perform_create(serializer)
        except IntegrityError:
            return Response(data={'error': 'This post is already liked by you'}, status=status.HTTP_400_BAD_REQUEST)



