from rest_framework import generics
from ..serializers import PostSerializer
from ..models import Post
from rest_framework.permissions import IsAuthenticated


class PostCreationAPIView(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)
