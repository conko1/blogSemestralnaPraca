from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.BlogView.as_view(), name='blogs'),
    path('new/', views.BlogCreateView.as_view(), name='create'),
    path('<int:pk>/', views.BlogDetailView.as_view(), name='detail'),
    path('my/', views.UserRelatedBlogsView.as_view(), name='user_specific'),
    path('liked/', views.UserLikedBlogsView.as_view(), name='liked'),
]
