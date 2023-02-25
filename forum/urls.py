from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('posts/', views.PostList.as_view(), name='posts'),
    path('createpost/', views.CreatePost.as_view(), name='create_post'),
    path('updatepost/<slug:slug>', views.UpdatePost.as_view(),
         name='updatepost'),
    path('deletepost/<slug:slug>', views.DeletePost.as_view(),
         name='deletepost'),
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path('like/<slug:slug>', views.PostLike.as_view(), name='post_like'),
]
