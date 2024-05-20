from rest_framework import serializers
from django.utils import timezone
from django.core.validators import EmailValidator
from geeks_tools.models import *

from django.contrib.auth import get_user_model
User = get_user_model()


from rest_framework import serializers


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')
        read_only_fields = ('id',)


class SubcategorySerializer(serializers.ModelSerializer):
    category = CategoryListSerializer()

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
    




class SubcategorylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = ('id', 'name') 
        read_only_fields = ('id',)


class HashtagSerializer(serializers.ModelSerializer):
    subcategories = SubcategorylistSerializer()

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






        









class UserToolSerializer(serializers.ModelSerializer):
    # category = CategorySerializer()
    hashtags = HashtagSerializer(many=True)

    class Meta:
        model = User_tool
        fields = ('id', 'user', 'name', 'logo', 'url', 'intro', 'pricing', 'category', 'hashtags', 'created_at')
        read_only_fields = ('id', 'user')

    def create(self, validated_data):
        user = self.context['request'].user

        category_data = validated_data.pop('category')
        category, created = Category.objects.get_or_create(**category_data)

        hashtags_data = validated_data.pop('hashtags', [])

        user_tool = User_tool.objects.create(user=user, category=category, **validated_data)

        for hashtag_data in hashtags_data:
            hashtag, created = Hashtag.objects.get_or_create(user_tools=user_tool, **hashtag_data)

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
    




class PostSerializer(serializers.ModelSerializer):
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


    















# def create(self, validated_data):
    #     hashtag, created = Hashtag.objects.get_or_create( **validated_data)
    #     return hashtag

