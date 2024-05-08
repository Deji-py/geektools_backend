from django.urls import path
from . import views_main
from . import views_admin


urlpatterns = [
    
    path('category/', views_main.categoriesList, name='category'),  
    path('hashtag/', views_main.createHashtag, name='hashtag'),
    path('user-tool/', views_main.user_tool_creation, name='user-tool'),
    path('setup/', views_main.create_setup, name='setup'),
    path('tool-info/', views_main.create_tool_info, name='tool-info'),
    path('subcription/', views_main.email_subcription, name='subcription'),
    path('blog-post/', views_main.blog_post, name='blog-post'),
    path('create-post/', views_admin.create_post, name='create-post'),
    path('post-details/<int:pk>/', views_admin.update_post, name='post-details'),

]
