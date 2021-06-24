from django.db.models import Count
from rest_framework import generics, status
from django_filters import rest_framework as filters

from api.models import Reaction
from rest_framework.response import Response

from .filters import PostFilter
from .serializers import AnalyticsReactionSerializer


class ReactionAnalyticsAPIView(generics.ListAPIView):
    queryset = Reaction.objects.all()
    serializer_class = AnalyticsReactionSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = PostFilter

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()).values('created_at').annotate(amount=Count('id'))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
