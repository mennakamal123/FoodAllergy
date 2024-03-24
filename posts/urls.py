from django.urls import path, include
from rest_framework import routers
from .views import PublicPostViewSet, CommentViewSet, PostViewSet, UserPostsViewSet, PostCommentsViewSet, ContactMessageView
from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()
router.register('posts', PublicPostViewSet, basename='Posts')
router.register('addposts', PostViewSet, basename='Posts')
router.register('comments', CommentViewSet, basename='Comments')
router.register('user-posts/(?P<user_id>[^/.]+)', UserPostsViewSet, basename='user-posts')
router.register('posts/(?P<post_id>\d+)/comments', PostCommentsViewSet, basename='post-comments')

urlpatterns = [
    path('', include(router.urls)),
    path('contact/', ContactMessageView.as_view(), name='contact'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)