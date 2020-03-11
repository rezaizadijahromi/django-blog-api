from rest_framework import filters
from rest_framework import generics
from rest_framework import permissions

from django.db.models import Q

from posts.models import Post

from .serializers import PostCreateUpdateSerializer, PostDetailSerializer, PostListSerializer
from .permissions import IsOwnerOrReadOnly

class PostCreateAPIView(generics.CreateAPIView):

    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateSerializer

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

class PostDetailAPIView(generics.RetrieveAPIView):

    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    lookup_field = 'slug'
    permission_classes = (permissions.AllowAny,)

class PostUpdateAPIView(generics.RetrieveUpdateAPIView):

    queryset = Post.objects.all()
    serializer_class = PostCreateAPIView
    lookup_field = 'slug'
    permission_classes = (IsOwnerOrReadOnly)

    def perform_update(self, serializer):
        return serializer.save(user=self.request.user)

class PostDeleteAPIView(generics.RetrieveDestroyAPIView):

    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    lookup_field = 'slug'
    permission_classes = (IsOwnerOrReadOnly,)


class PostListAPIView(generics.ListAPIView):

    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    lookup_class = 'slug'
    permission_clases = (permissions.AllowAny)
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    serach_fields = ('title', 'content', 'user__first_name')

    def get_queryset(self):

        query_list = Post.objects.all()
        query = self.request.GET.get('q')
        if query:
            query_list = query_list.filter(
                Q(title__icontains=query)|
                Q(user__first_name__icontains=query)|
                Q(user__last_name__icontains=query)|
                Q(content__icontains=query)
            ).distinct()
            return query_list

