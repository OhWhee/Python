from django.urls import path
from .views import *

urlpatterns = [
    path('', posts_list, name='posts_list_url'),
    path('posts/<str:slug>/', post_detail, name='post_detail_url'),
    path('tags/', tag_list, name='tag_list_url'),
    path('tag/<str:slug>/', tag_detail, name='tag_detail_url')
]
