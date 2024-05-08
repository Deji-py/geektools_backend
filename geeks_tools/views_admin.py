from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view,permission_classes,parser_classes
from rest_framework.permissions import IsAuthenticated,IsAdminUser,AllowAny,IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from django.contrib.auth.models import Group
from geeks_tools.serializers import CategorySerializer,HashtagSerializer,UserToolSerializer,SetUpSerializer,ToolInfoSerializer,SubscriptionSerializer,PostSerializer
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser

from django.contrib.auth import get_user_model
User = get_user_model()
from geeks_tools.models import *



#ADMINISTRATION USERS VIEW



@api_view(['GET','POST'])
@permission_classes([IsAdminUser])
@parser_classes([FormParser, MultiPartParser])
def create_post(request):
    if request.method == 'GET':
        post= Post.objects.all()
        serializer = PostSerializer(post, many=True)
        return Response(serializer.data)


    elif request.method == 'POST':
        serializer = PostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'details': 'Blog post created successfully'}, status=status.HTTP_201_CREATED)
    return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)



@api_view(['PUT','PATCH','DELETE'])
@permission_classes([IsAdminUser])
@parser_classes([FormParser, MultiPartParser])
def update_post(request, pk):
    try:
        post = Post.objects.get(id=pk)
    except Post.DoesNotExist:
        return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = PostSerializer(post, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'details': 'Blog post updated successfully'})
    

    elif request.method == 'PATCH':
        serializer = PostSerializer(post, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'details': 'Blog post updated successfully'})
    
    
    elif  request.method == 'DELETE':
        post.delete()
        return Response({'details': 'Blog post deleted successfully'}, status=status.HTTP_204_NO_CONTENT)