from rest_framework import viewsets
from .serializers import (PostSerializer, GroupSerializer, UserSerializer,
                          CommentSerializer, FollowSerializer)
from posts.models import Post, Group, User, Comment
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework import filters
from rest_framework.pagination import LimitOffsetPagination
from .permissions import OwnerOrReadOnly
from django.shortcuts import get_object_or_404
from rest_framework import mixins


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.select_related('group').all()
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (OwnerOrReadOnly, IsAuthenticatedOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (OwnerOrReadOnly, IsAuthenticatedOrReadOnly)

    def get_queryset(self):
        post_id = self.kwargs.get("post_id")
        post = get_object_or_404(Post, id=post_id)
        new_queryset = Comment.objects.select_related(
            'post').filter(post=post)
        return new_queryset

    def perform_create(self, serializer):
        post_id = self.kwargs.get("post_id")
        post = get_object_or_404(Post, id=post_id)
        serializer.save(author=self.request.user,
                        post=post)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class FollowActionsViewSet (mixins.CreateModelMixin,
                            mixins.ListModelMixin,
                            mixins.RetrieveModelMixin,
                            viewsets.GenericViewSet):
    pass


class FollowViewSet(FollowActionsViewSet):
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated, )
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        return self.request.user.following.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
