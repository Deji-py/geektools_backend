from rest_framework import serializers
from django.utils import timezone
from .models import *

from django.contrib.auth import get_user_model
User = get_user_model()



# Serializer for user registration
class RegisterUserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'password', 'password2')
        extra_kwargs = {'password': {'write_only':True}}


    # Validate the password confirmation
    def validate(self, attrs):
        password = attrs.get('password', '')
        password2 = attrs.get('password2')
        
        if password != password2:
            raise serializers.ValidationError("password and confirm password doesn't match")
        return attrs
    
     # Create method to handle user creation
    def create(self, validated_data):
        validated_data.pop('password2', None)

        # Extract the password from validated_data
        password = validated_data.pop('password')

        user = User.objects.create(**validated_data)
        # Use Django's set_password method to hash and set the password
        user.set_password(password)
        # Save the user object with the hashed password
        user.save()
        return user
    
    
# Serializer for changing user password
class changePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, max_length=255, style={'input_type': 'password'}, write_only=True)
    new_password = serializers.CharField(required=True, max_length=255, style={'input_type': 'password'}, write_only=True)
    confirm_password = serializers.CharField(required=True, max_length=255, style={'input_type': 'password'}, write_only=True)

    def validate(self, attrs):
        old_password = attrs.get('old_password')
        new_password = attrs.get('new_password')
        confirm_password = attrs.get('confirm_password')
        user = self.context.get('user')


         # Check if the old password matches the user's current password
        if not user.check_password(old_password):
            raise serializers.ValidationError('Old password is incorrect')

        # check that the new password and confirmation match
        if new_password != confirm_password:
            raise serializers.ValidationError("New Password and Confirm Password don't match")

        if len(new_password) <= 6:
            raise serializers.ValidationError("Weak Password")
        
        # Set the new password for the user
        user.set_password(new_password)
        user.save()
        return attrs





# Serializer for resetting user password via email
class resetPasswordEmailSerializer(serializers.Serializer):
    email=serializers.EmailField(required=True, max_length=50, style={'input_type':'email'}, write_only=True)






class VerificationCodeSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=6)




class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['user', 'email', 'first_name', 'last_name', 'gender', 'profile_picture', 'country', 'state', 'date_created', 'date_updated']
        extra_kwargs = {
            'email': {'read_only': True},
        }
        read_only_fields = ['date_created', 'date_updated', 'user']

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.profile_picture = validated_data.get('profile_picture', instance.profile_picture)
        instance.country = validated_data.get('country', instance.country)
        instance.state = validated_data.get('state', instance.state)
        instance.state = validated_data.get('state', instance.state)  # Add this line for the 'state' field

        # Update the 'updated_created' field to the current timestamp
        instance.date_updated = timezone.now()

        instance.save()
        return instance

