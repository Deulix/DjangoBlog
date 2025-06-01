from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('post/new/', views.post_create, name='post_create'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),
    path('register/', views.register, name='register'),
    path('post/<int:pk>/like/', views.post_like, name='post_like'),
    path('comment/<int:pk>/like/', views.comment_like, name='comment_like'),
    # path('profile/<int:pk>/', views.profile, name='profile'),

    
]
