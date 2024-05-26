from django.urls import path
from . import views_main
from . import views_admin
from .views_main import UserToolList,UserPostList


urlpatterns = [
    
    path('category/', views_main.categorty_list, name='category'),  
    path('hashtags/', views_main.hashtag_list, name='hashtags'),
    path('user-tool/', views_main.user_tool_creation, name='user-tool'),
    path('setup/', views_main.create_setup, name='setup'),
    path('tool-info/', views_main.create_tool_info, name='tool-info'),
    path('subcription/', views_main.email_subcription, name='subcription'),
    path('blog-post/', views_main.blog_post, name='blog-post'),
    path('user-tool-list/', UserToolList.as_view(), name='user-tool-list'),
    path('post-list/', UserPostList.as_view(), name='post-list'),
    path('bookmarks/',  views_main.bookmark_list_create, name='bookmark-list-create'),
    path('bookmarks/<int:pk>/',  views_main.bookmark_detail, name='bookmark-detail'),

    path('create-post/', views_admin.create_post, name='create-post'),
    path('post-details/<int:pk>/', views_admin.update_post, name='post-details'),
    path('sub-categories/', views_admin.sub_category_view, name='sub-categories'), 
    path('sub-category/<int:pk>/', views_admin.update_subcategory_view, name='sub-category'),
    path('admin-hashtags/', views_admin.hashtag_view, name='admin-hashtags'),
    path('update-admin-hashtag/<int:pk>/', views_admin.update_hashtag_view, name='update-admin-hashtag'),

    
]
