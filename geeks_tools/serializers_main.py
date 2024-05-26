from rest_framework import serializers
from django.utils import timezone
from django.core.validators import EmailValidator
from geeks_tools.models import *

from django.contrib.auth import get_user_model
User = get_user_model()



#List of all Category with all its fields
class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')
        read_only_fields = ('id',)


#Nested Category,subcategory,hashtag on user_tool
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')
        read_only_fields = ('id',)


class SubcategorylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = ('id', 'name') 
        read_only_fields = ('id',)


class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = ('id', 'term')
        read_only_fields = ('id',)


class UserToolSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    subcategory = SubcategorylistSerializer()
    hashtag = HashtagSerializer(many=True)
    

    class Meta:
        model = User_tool
        fields = ('id', 'user', 'name', 'url', 'intro', 'pricing', 'category', 'subcategory', 'hashtag', 'created_at')
        read_only_fields = ('id', 'user', 'created_at')


    def validate(self, data):
        category_name = data['category']['name']
        subcategory_name = data['subcategory']['name']
        hashtags = data.get('hashtag', [])
        url = data.get('url')


        if User_tool.objects.filter(url=url).exists():
            raise serializers.ValidationError(f"The URL '{url}' is already in use by another tool.")


        try:
            category = Category.objects.get(name=category_name)
        except Category.DoesNotExist:
            raise serializers.ValidationError(f"Category '{category_name}' does not exist.")

        try:
            subcategory = Subcategory.objects.get(name=subcategory_name, category=category)
        except Subcategory.DoesNotExist:
            raise serializers.ValidationError(f"Subcategory '{subcategory_name}' does not exist in category '{category_name}'.")

        for hashtag_data in hashtags:
            hashtag_term = hashtag_data.get('term')
            if not Hashtag.objects.filter(term=hashtag_term, subcategories=subcategory).exists():
                raise serializers.ValidationError(f"Hashtag '{hashtag_term}' does not exist for subcategory '{subcategory_name}'.")

        return data


    def create(self, validated_data):
        user = self.context['request'].user

        # Extract category data and create or get Category object
        category_data = validated_data.pop('category')
        category_name = category_data.get('name')
        category, created = Category.objects.get_or_create(name=category_name)

        # Extract subcategory data and create or get Subcategory object
        subcategory_data = validated_data.pop('subcategory')
        subcategory_name = subcategory_data.get('name')
        subcategory, created = Subcategory.objects.get_or_create(name=subcategory_name, category=category)

        # Extract hashtags data and create or get Hashtag objects
        hashtags_data = validated_data.pop('hashtag', [])
        user_tool = User_tool.objects.create(user=user, category=category, subcategory=subcategory, **validated_data)

        for hashtag_data in hashtags_data:
            hashtag_term = hashtag_data.get('term')
            hashtag, created = Hashtag.objects.get_or_create(term=hashtag_term)
            user_tool.hashtag.add(hashtag)

        return user_tool



 





#Nested serializer with the user_tool to access the Bookmark
# class ToolSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User_tool
#         fields = ('id', 'name','url','intro','pricing')

class BookmarkSerializer(serializers.ModelSerializer):
    user_tool = UserToolSerializer(read_only=True)
    user_tool_id = serializers.PrimaryKeyRelatedField(
        queryset=User_tool.objects.all(), source='user_tool', write_only=True
    )

    class Meta:
        model = Bookmark
        fields = ('id', 'user', 'user_tool', 'user_tool_id', 'created_at')
        read_only_fields = ('id', 'user', 'created_at')

    def validate(self, data):
        user = self.context['request'].user
        user_tool = data['user_tool']
        
        if Bookmark.objects.filter(user=user, user_tool=user_tool).exists():
            raise serializers.ValidationError("You have already bookmarked this tool.")
        
        return data

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)



    

#Setup serializer
class SetUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = SetUp
        fields = ('id', 'user', 'package_name', 'features', 'Pricing', 'timeline')
        read_only_fields =('id', 'user')

    def validate_features(self, value):
        """
        Validate that the number of features does not exceed 10.
        """
        if len(value) > 10:
            raise serializers.ValidationError("Number of features cannot exceed 10.")
        return value



    def create(self, validated_data):

        user = self.context['request'].user
        setup = SetUp.objects.create(user=user, **validated_data)
        return setup
    


   

#Nested Serializer with the social Link on the tool Info
class SocialLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialLinks
        fields = ('id', 'name', 'link')
        read_only_fields= ['id']



class ToolInfoSerializer(serializers.ModelSerializer):
    links = SocialLinkSerializer(many=True) 

    class Meta:
        model = ToolInfo
        fields = ('id', 'user', 'description', 'images', 'agent', 'features','video', 'links')
        read_only_fields = ['id', 'user']

    def validate_features(self, value):
        """
        Validate that the number of features does not exceed 10.
        """
        if len(value) > 10:
            raise serializers.ValidationError("Number of features cannot exceed 10.")
        return value 

    def create(self, validated_data):
        user = self.context['request'].user
        links_data = validated_data.pop('links')
        tool_info = ToolInfo.objects.create(user=user, **validated_data)
        for link_data in links_data:
            link = SocialLinks.objects.create(**link_data)
            tool_info.links.add(link)
        return tool_info



#Subcription Serializer
class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['id', 'email', 'subscribed_at', 'is_subscribed']
        read_only_fields = ['id', 'subscribed_at']

    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError("Email cannot be empty")
        
        email_validator = EmailValidator()
        try:
            email_validator(value)
        except serializers.ValidationError:
            raise serializers.ValidationError("Invalid email format")

        subscribed = Subscription.objects.filter(email=value).first()
        if subscribed:
            raise serializers.ValidationError("Email already registered, please use a different email")

        return value 

    def validate_is_subscribed(self, value):
        if not isinstance(value, bool):
            raise serializers.ValidationError("Subscription status must be a boolean value")
        return value

    def create(self, validated_data):
        return Subscription.objects.create( **validated_data)
    


#Post Serializer
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title',  'content', 'status', 'image', 'likes', 'created_on', 'updated_on']
        read_only_fields = ['id','created_on', 'updated_on'] 

