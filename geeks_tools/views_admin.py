from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view,permission_classes,parser_classes
from rest_framework.permissions import IsAuthenticated,IsAdminUser,AllowAny,IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from django.contrib.auth.models import Group
from geeks_tools.serializers_admin import AdminCategorySerializer,AdminSubcategorySerializer,AdminPostSerializer,AdminHashtagSerializer
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser

from django.contrib.auth import get_user_model
User = get_user_model()
from geeks_tools.models import *




#ADMINISTRATION USERS VIEW
@api_view(['GET'])
@permission_classes([IsAdminUser])
def categoriesList(request):
    categories = Category.objects.all()
    serializer = AdminCategorySerializer(categories, many=True)
    return Response(serializer.data)




@api_view(['GET','POST'])
@permission_classes([IsAdminUser])
def createHashtag(request):
    if request.method == 'GET':
        hashtag = Hashtag.objects.all()
        serializer = AdminHashtagSerializer(hashtag, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = AdminHashtagSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





@api_view(['GET','POST'])
@permission_classes([IsAdminUser])
def sub_category_view(request):
    if request.method == 'GET':
        sub_category=Subcategory.objects.all()
        serializer = AdminSubcategorySerializer(sub_category, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = AdminSubcategorySerializer(data=request.data, context={'request':request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'sub category created successfully'}, status=status.HTTP_201_CREATED)
    return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)





@api_view(['PUT', 'DELETE'])
@permission_classes([IsAdminUser])
def update_subcategory_view(request, pk):
    try:
        sub_category = Subcategory.objects.get(id=pk)
    except Subcategory.DoesNotExist:
        return Response({'error': 'Subcategory not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'PUT':
        serializer = AdminSubcategorySerializer(sub_category, data=request.data, partial=True) 
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Subcategory updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        sub_category.delete()
        return Response({'message': 'Subcategory deleted successfully'}, status=status.HTTP_204_NO_CONTENT)





@api_view(['GET','POST'])
@permission_classes([IsAdminUser])
def hashtag_view(request):
    if request.method == 'GET':
        hash_tag=Hashtag.objects.all()
        serializer = AdminHashtagSerializer(hash_tag, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = AdminHashtagSerializer(data=request.data, context={'request':request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'hashtag created successfully'}, status=status.HTTP_201_CREATED)
    return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)





@api_view(['PUT', 'DELETE'])
@permission_classes([IsAdminUser])
def update_hashtag_view(request, pk):
    try:
        hashtag = Hashtag.objects.get(pk=pk)
    except Hashtag.DoesNotExist:
        return Response({'error': 'Hashtag not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'PUT':
        serializer = AdminHashtagSerializer(hashtag, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Hashtag updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        hashtag.delete()
        return Response({'message': 'Hashtag deleted successfully'}, status=status.HTTP_204_NO_CONTENT)






@api_view(['GET','POST'])
@permission_classes([IsAdminUser])
@parser_classes([FormParser, MultiPartParser])
def create_post(request):
    if request.method == 'GET':
        post= Post.objects.all()
        serializer = AdminPostSerializer(post, many=True)
        return Response(serializer.data)


    elif request.method == 'POST':
        serializer = AdminPostSerializer(data=request.data)
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
        serializer = AdminPostSerializer(post, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'details': 'Blog post updated successfully'})
    

    elif request.method == 'PATCH':
        serializer = AdminPostSerializer(post, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'details': 'Blog post updated successfully'})
    
    
    elif  request.method == 'DELETE':
        post.delete()
        return Response({'details': 'Blog post deleted successfully'}, status=status.HTTP_204_NO_CONTENT)