from django.contrib import admin
from geeks_tools.models import Category, Hashtag, User_tool, SetUp, SocialLinks, ToolInfo, Subscription
from .models import User
from django.contrib.auth import get_user_model
User = get_user_model()

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']



@admin.register(Hashtag)
class HashtagAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']



@admin.register(User_tool)
class UserToolAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'intro', 'pricing']
    search_fields = ['name']
    list_filter = ['pricing']




@admin.register(SetUp)
class SetUpAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'package_name','features','Pricing','timeline']
    search_fields = ['package_name']
    list_filter = ['timeline']



@admin.register(SocialLinks)
class SocialLinksAdmin(admin.ModelAdmin):
    list_display = ['name', 'link']
    search_fields = ['name', 'link']



@admin.register(ToolInfo)
class ToolInfoAdmin(admin.ModelAdmin):
    list_display = ['user', 'description', 'images', 'agent', 'features', 'video', 'display_links']
    search_fields = ['user__first_name', 'description', 'agent', 'features']

    def display_links(self, obj):
        return ', '.join([link.name for link in obj.links.all()])

    display_links.short_description = 'Links'


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['email', 'subscribed_at', 'is_subscribed']
    list_filter = ['is_subscribed']
    search_fields = ['email']

admin.site.register(Subscription, SubscriptionAdmin)