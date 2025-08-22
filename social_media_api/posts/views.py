from rest_framework import generics, status
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer, LikeSerializer
from notifications.models import Notification
from notifications.serializers import NotificationSerializer

# Create your views here.
class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow authors of an object to edit or delete it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions are only allowed to the author of the object.
        return obj.author == request.user

class PostViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and managing posts.
    """
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'updated_at']

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            # include posts from the user + people they follow
            following_users = user.following.all()
            return Post.objects.filter(author__in=following_users).order_by('-created_at')
        # for unauthenticated users, return all posts (or empty if you prefer stricter privacy)
        return Post.objects.all().order_by('-created_at')

    def perform_create(self, serializer):
        # The author is automatically set to the current user on creation
        serializer.save(author=self.request.user)

    # Custom action to get comments for a specific post
    # This will create a URL like /posts/{id}/comments/
    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        post = self.get_object()
        comments = post.comments.all().order_by('-created_at')
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

class CommentViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and managing comments.
    """
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        # The author is automatically set to the current user on creation
        serializer.save(author=self.request.user)

class LikePostView(generics.GenericAPIView):
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if created:
            # Create notification for post author
            if request.user != post.author:
                Notification.objects.create(
                    recipient=post.author,
                    actor=request.user,
                    verb="liked your post",
                    target=post,
                )
            return Response({"message": "Post liked!"}, status=status.HTTP_201_CREATED)
        return Response({"message": "You already liked this post"}, status=status.HTTP_400_BAD_REQUEST)


class UnlikePostView(generics.GenericAPIView):
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        like = Like.objects.filter(user=request.user, post=post).first()
        if like:
            like.delete()
            return Response({"message": "Post unliked!"}, status=status.HTTP_200_OK)
        return Response({"message": "You haven’t liked this post yet"}, status=status.HTTP_400_BAD_REQUEST)

