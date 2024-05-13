from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator

User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='category_images/', validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])])

    def __str__(self):
        return self.name



class Hashtag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    

PRICING_CHOICES = (
    ('Free', 'Free'),
    ('Freemium', 'Freemium'),
    ('Premium', 'Premium'),
)

class User_tool(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='logos/', validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])], blank=True, null=True)
    url = models.URLField()
    intro = models.CharField(max_length=70)
    hashtag = models.ManyToManyField(Hashtag, related_name='user_tools')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='user_tools')
    pricing = models.CharField(max_length=10, choices=PRICING_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Tool created by {self.user.first_name}"
    




TIMELINE_CHOICES = (
    ('Monthly', 'Monthly'),
    ('Yearly', 'Yearly'),
    ('Annually', 'Annually'),
)

class SetUp(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    package_name = models.CharField(max_length=30)
    features = models.JSONField()
    Pricing= models.CharField(max_length=20)
    timeline = models.CharField(max_length=10, choices=TIMELINE_CHOICES)

    def __str__(self):
        return self.package_name
    


class SocialLinks(models.Model):
    name= models.CharField(max_length=20)
    link=models.URLField()

    def __str__(self):
        return self.name



class ToolInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    description = models.TextField()
    images = models.ImageField(upload_to='logos/', validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])],blank=True, null=True)
    agent = models.CharField(max_length=100)
    video=models.URLField()
    features = models.JSONField()
    links = models.ManyToManyField(SocialLinks, related_name='tools')  

    def __str__(self):
        if self.user:
            return f"Tool Information for {self.user.first_name}"
        else:
            return "Tool Information"




class Subscription(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_subscribed = models.BooleanField(default=True)

    def __str__(self):
        return self.email
    





STATUS = (
    ('Draft', 'Draft'),
    ('Publish', 'Publish')
)

class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    content = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS, default='Draft')
    image = models.ImageField(null=True, blank=True)
    likes = models.IntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_on']
    

    def save(self, *args, **kwargs):
        # Custom logic to set default values
        if not self.status:
            self.status = 'Draft'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    


    
    














