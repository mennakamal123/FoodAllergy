from rest_framework import viewsets, permissions
from .models import Post, Comment, ContactMessage
from .serializers import PostSerializer, CommentSerializer, ContactMessageSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated , IsAuthenticatedOrReadOnly
from .permissions import IsDoctor, IsOwnerOrStaffOrReadOnly
from rest_framework.views import APIView

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [SearchFilter]
    search_fields = ['allergy__arabicName', 'allergy__englishName']
    permission_classes = [IsAuthenticated, IsOwnerOrStaffOrReadOnly]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
    
    
class PublicPostViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [SearchFilter]
    search_fields = ['allergy__arabicName', 'allergy__englishName']
    permission_classes = [IsAuthenticatedOrReadOnly]
    @action(
        detail=True, methods=['POST'],
        serializer_class=None,
        permission_classes=[IsAuthenticated],)
    def like(self, request,pk=None):
        post = self.get_object()
        user = request.user

        if user in post.likes.all():
            post.likes.remove(user)
            liked = False
        else:
            post.likes.add(user)
            liked = True
        post.save()
        return Response({'liked': liked})

class UserPostsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Post.objects.filter(owner__id=user_id)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsDoctor]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class PostCommentsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Comment.objects.filter(post__id=post_id)

class ContactMessageView(APIView):
    queryset = ContactMessage.objects.all()
    serializer_class =ContactMessageSerializer
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = ContactMessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Thank you for your message! We will get back to you soon.'}, status=201)
        return Response(serializer.errors, status=400)