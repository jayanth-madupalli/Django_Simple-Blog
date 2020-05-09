from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostListView.as_view(), name='Blog-Home'),
    path('user/<str:username>', views.UserPostListView.as_view(), name='User-Posts'),
    path('post/<int:pk>-<title>/', views.PostDetailView.as_view(), name='Post-Detail'),
    path('post/update/<int:pk>/', views.PostUpdateView.as_view(), name='Post-Update'),
    path('post/delete/<int:pk>/', views.PostDeleteView.as_view(), name='Post-Delete'),
    path('post/new/', views.PostCreateView.as_view(), name='Post-Create'),
]