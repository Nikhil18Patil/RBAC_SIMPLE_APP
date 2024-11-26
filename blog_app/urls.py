from django.urls import path
from .views import PostView, CommentView

urlpatterns = [
    path('posts/', PostView.as_view(), name='posts'),
    path('posts/<uuid:pk>/', PostView.as_view(), name='post_detail'),
    path('comments/', CommentView.as_view(), name='comments'),
]
