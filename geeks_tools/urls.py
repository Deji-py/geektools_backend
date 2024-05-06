from django.urls import path
from . import views



urlpatterns = [
    
    path('category/', views.categoriesList, name='category'),  
    path('hashtag/', views.createHashtag, name='hashtag'),
    path('user-tool/', views.user_tool_creation, name='user-tool'),
    path('setup/', views.create_setup, name='setup'),
    path('tool-info/', views.create_tool_info, name='tool-info'),
    path('subcription/', views.email_subcription, name='subcription'),


]