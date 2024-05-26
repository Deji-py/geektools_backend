from django.shortcuts import render
from rest_framework import status
from rest_framework import generics
from rest_framework.decorators import api_view,permission_classes,parser_classes
from rest_framework.permissions import IsAuthenticated,IsAdminUser,AllowAny,IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from django.contrib.auth.models import Group
from geeks_tools.serializers_main import CategoryListSerializer,HashtagSerializer,UserToolSerializer,SetUpSerializer,ToolInfoSerializer,SubscriptionSerializer,PostSerializer,BookmarkSerializer
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser
from django_filters.rest_framework import DjangoFilterBackend

from django.contrib.auth import get_user_model
User = get_user_model()
from geeks_tools.models import *

# Create your views here.

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def categorty_list(request):
    category = Category.objects.all()
    serializer = CategoryListSerializer(category, many=True)
    return Response(serializer.data)


@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def hashtag_list(request):
    hashtag = Hashtag.objects.all()
    serializer = HashtagSerializer(hashtag, many=True)
    return Response(serializer.data)

    

@api_view(['GET','POST'])
# @permission_classes([IsAuthenticated])
# @parser_classes([FormParser, MultiPartParser])
def user_tool_creation(request):
    if request.method == 'GET':
        tool = User_tool.objects.all()
        serializer = UserToolSerializer(tool, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = UserToolSerializer(data=request.data, context={'request':request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"detail": "Tools created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def bookmark_list_create(request):
    if request.method == 'GET':
        bookmarks = Bookmark.objects.filter(user=request.user)
        serializer = BookmarkSerializer(bookmarks, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = BookmarkSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def bookmark_detail(request, pk):
    bookmark = get_object_or_404(Bookmark, pk=pk, user=request.user)

    if request.method == 'GET':
        serializer = BookmarkSerializer(bookmark)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        bookmark.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def create_setup(request):
    if request.method == 'GET':
        set_up = SetUp.objects.all() 
        serializer = SetUpSerializer(set_up, many=True)
        return Response(serializer.data)


    elif request.method == 'POST':
        serializer = SetUpSerializer(data=request.data, context={'request':request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"detail": "SetUp completed successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            


@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def create_tool_info(request):
    if request.method == 'GET':
        tool_info = ToolInfo.objects.all() 
        serializer = ToolInfoSerializer(tool_info, many=True)
        return Response(serializer.data)


    elif request.method == 'POST':
        serializer = ToolInfoSerializer(data=request.data, context={'request':request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"detail": "SetUp completed successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['POST'])
def email_subcription(request):
    if request.method == 'POST':
        serializer = SubscriptionSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"detail": "Email Subcription was successful"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def blog_post(request):
    post= Post.objects.filter(status='Publish')
    serializer = PostSerializer(post, many=True)
    return Response(serializer.data)




class UserToolList(generics.ListAPIView):
    queryset = User_tool.objects.all()
    serializer_class = UserToolSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name','intro','hashtag','pricing','category']



class UserPostList(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title']









