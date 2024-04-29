from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group
from django.utils import timezone
from django.core.validators import FileExtensionValidator


class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        """
        Creates, saves and returns a User with the given email, username, and password.
        """

        if not email:
            raise ValueError('User must have an email address')
        if not first_name:
            raise ValueError('First name is required')
        if not last_name:
            raise ValueError('Last name is required')

        user = self.model(first_name=first_name, last_name=last_name, email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, first_name, last_name, password=None):
        """
        Creates, saves, and returns a superuser with the given email, username, and password.
        """

        if password is None:
            raise ValueError('Password should not be none')

        user = self.create_user(email, first_name, last_name, password)
        user.is_superuser = True
        user.is_staff = True
        user.is_verified = True
        user.save()
        return user


AUTH_PROVIDERS = {'email': 'email', 'google': 'google'}


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    groups = models.ManyToManyField(Group, blank=True)
    auth_provider = models.CharField(max_length=50, blank=False, null=False, default=AUTH_PROVIDERS.get('email'))

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.email}"

    @property
    def get_full_name(self):
        return f"{self.first_name} - {self.last_name}"


class UserRole(models.Model):
    name = models.CharField(max_length=20, blank=True, null=True, unique=True)

    def __str__(self):
        return self.name


GENDER_CHOICES = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Others', 'Others'),
)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(unique=True, null=True, blank=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, null=True)
    profile_picture = models.ImageField(upload_to='profile_images/', validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])])
    country = models.CharField(max_length=50, null=True)
    role = models.OneToOneField(UserRole, on_delete=models.CASCADE)
    company = models.CharField(max_length=50, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"User Profile for {self.user.first_name}"

    class Meta:
        ordering = ['-date_created']


class  OneTimePassword(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6) 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name}-passcode"