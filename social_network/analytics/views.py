from rest_framework import generics

from api.models import Reaction
from api.serializers import ReactionSerializer


class ReactionAnalyticsAPIView(generics.ListAPIView):
    queryset = Reaction.objects.all()
    serializer_class = ReactionSerializer
