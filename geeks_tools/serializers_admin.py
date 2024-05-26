from rest_framework import serializers
from django.utils import timezone
from django.core.validators import EmailValidator
from geeks_tools.models import *

from django.contrib.auth import get_user_model
User = get_user_model()


from rest_framework import serializers

class AdminCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')
        read_only_fields = ('id',)

    def create(self, validated_data):
        return Category.objects.create(**validated_data)




class AdminCategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')
        read_only_fields = ('id',)


class  AdminSubcategorySerializer(serializers.ModelSerializer):
    category = AdminCategoryListSerializer()

    class Meta:
        model = Subcategory
        fields = ('id', 'name', 'category')
        read_only_fields = ('id',)

    def create(self, validated_data):
        category_data = validated_data.pop('category')
        category_name = category_data.get('name')
        category, created = Category.objects.get_or_create(name=category_name)
        sub_category = Subcategory.objects.create(category=category, **validated_data)
        return sub_category

    
    def update(self, instance, validated_data):
        category_data = validated_data.pop('category')
        category_name = category_data.get('name')
        category, created = Category.objects.get_or_create(name=category_name)

        instance.category = category

        instance.name = instance.name = validated_data.get('name', instance.name)

        instance.save()
        return instance
    




class AdminSubcategorylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = ('id', 'name') 
        read_only_fields = ('id',)


class AdminHashtagSerializer(serializers.ModelSerializer):
    subcategories = AdminSubcategorylistSerializer()

    class Meta:
        model = Hashtag
        fields = ('id', 'term', 'subcategories')
        read_only_fields = ('id',)

    def validate(self, attrs):
        term = attrs.get('term')
        if term is not None and not term.startswith('#'):
            raise serializers.ValidationError("Hashtag term must start with '#'")
        return attrs
    
    def create(self, validated_data):
        subcategories_data = validated_data.pop('subcategories')
        subcategory_name = subcategories_data.get('name')

        subcategory, created = Subcategory.objects.get_or_create(name=subcategory_name)
        hashtag = Hashtag.objects.create(subcategories=subcategory, **validated_data)
        
        return hashtag


    def update(self, instance, validated_data):
        subcategories_data = validated_data.pop('subcategories')
        subcategory_name = subcategories_data.get('name')

        subcategory, created = Subcategory.objects.get_or_create(name=subcategory_name)
        instance.subcategories = subcategory

        instance.term = validated_data.get('term', instance.term)

        instance.save()
        return instance




class AdminPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title',  'content', 'status', 'image', 'likes', 'created_on', 'updated_on']
        read_only_fields = ['id','created_on', 'updated_on'] 

    def create(self, validated_data):
        return Post.objects.create( **validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.status = validated_data.get('status', instance.status)
        instance.image = validated_data.get('image', instance.image)
        instance.likes = validated_data.get('likes', instance.likes)
        instance.save()
        return instance
