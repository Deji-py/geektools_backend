from rest_framework import serializers
from django.utils import timezone
from django.core.validators import EmailValidator
from geeks_tools.models import *

from django.contrib.auth import get_user_model
User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'images')
        read_only_field = ('id')


class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = ('id', 'name')
        read_only_field = ('id')

    def validate(self,attr):
        name = attr.get('name')
        if not name.startswith('#'):
            raise serializers.ValidationError("Hashtag name must start with '#'")
        return attr
    
    


class UserToolSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True)
    hashtags = HashtagSerializer(many=True)

    class Meta:
        model = User_tool
        fields =('id','user','name', 'logo','url','intro','pricing','created_at', 'categories', 'hashtags')
        read_only_fields=('id','user')


    # Create the User_tool instance
    def create(self, validated_data):
        user = self.context['request'].user
        category_names = validated_data.pop('categories', [])
        hashtag_data = validated_data.pop('services', [])

        user_tool = User_tool.objects.create(user=user, **validated_data)
        
        # Create categories and add them to the User_tool instance
        for category_name in category_names:
            category, created = Category.objects.get_or_create(**category_name)
            user_tool.categories.add(category)


         # Create hashtags and add them to the User_tool instance
        for hashtag_item in hashtag_data:
            hashtag, created = Hashtag.objects.get_or_create(**hashtag_item)
            user_tool.hashtags.add(hashtag)

        return user_tool




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






    















# def create(self, validated_data):
    #     hashtag, created = Hashtag.objects.get_or_create( **validated_data)
    #     return hashtag

