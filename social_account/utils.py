from google.auth.transport import requests
from google.oauth2 import id_token
from django.contrib.auth import get_user_model
User = get_user_model()
from django.contrib.auth import authenticate
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed


class Google():
    @staticmethod
    def validate(access_token):
        try:
            # Verify the provided access token
            id_info = id_token.verify_oauth2_token(access_token, requests.request())
            if "account.google.com" in id_info['iss']:# Check if the issuer of the token is from "account.google.com"
                return id
        except Exception as e:
            return "Token is invalid or has expired"
        

def login_social_user(email, password):
    # Authenticate the user using the provided email and password
    user=authenticate(email=email, password=password)
     
    user_token=user.tokens() # Get the user's access and refresh tokens
    return{
        'email' : user.email,
        'full_name' : user.get_full_name,
        'access_token' : str(user_token.get('access')),
        'fresh_token' : str(user_token.get('refresh'))
    }


def register_social_user(provider, email, first_name, last_name):
    user=user.objects.filter(email=email)
    if user.exist():
         # Check if the provider matches the authentication provider of the existing user
        if provider == user[0].auth_provider:
            # If the provider matches, login the user using social authentication
            result=login_social_user(email, settings.SOCIAL_AUTH_PASSWORD)
            return result
        else:
            raise AuthenticationFailed(detail = f"please continue your login with {user[0].auth_provider}")
    else:
         # If a user with the provided email doesn't exist, create a new user
        new_user={
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
            'password':settings.SOCIAL_AUTH_PASSWORD
        }
        # Create a new user with the provided information
        register_user=user.objects.create_user(**new_user)
        register_user.auth_provider=provider
        register_user.is_verified=True
        register_user.save()
         # After user registration, login the user using social authentication
        result=login_social_user(email=register_user.email, password=settings.SOCIAL_AUTH_PASSWORD)
        return result
