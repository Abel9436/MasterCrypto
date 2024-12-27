from django.urls import path
from .views import RegisterEmailView, AirdropCreateView, AirdropListView,AirdropDetailView
from .views import BlogPostList, BlogPostDetail,feedback
urlpatterns = [
    path('register-email/', RegisterEmailView.as_view(), name='register-email'),
    path('add-airdrop/', AirdropCreateView.as_view(), name='add-airdrop'),
    path('airdrops/', AirdropListView.as_view(), name='airdrops'),
    path('airdrops/<int:pk>/', AirdropDetailView.as_view(), name='airdrop-detail'),
    path('posts/', BlogPostList.as_view(), name='post-list'),
    path('posts/<int:pk>/', BlogPostDetail.as_view(), name='post-detail'),
    path('feedback/', feedback, name='feedback'),
]
