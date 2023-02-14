from django.urls import path
from . import views

app_name = 'user_manager'
urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('', views.LoginView.as_view(), name='default'),
]
