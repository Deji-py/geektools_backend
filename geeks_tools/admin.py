from django.contrib import admin
from geeks_tools.models import Category, Hashtag, User_tool, SetUp, SocialLinks, ToolInfo, Subscription,Post,Subcategory,Bookmark
from .models import User
from django.contrib.auth import get_user_model
User = get_user_model()

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category')
    search_fields = ('name', 'category__name')
    list_filter = ('category',)

@admin.register(Hashtag)
class HashtagAdmin(admin.ModelAdmin):
    list_display = ('id', 'term', 'subcategories')
    search_fields = ('term', 'subcategories__name')
    list_filter = ('subcategories',)




@admin.register(User_tool)
class UserToolAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name', 'url', 'intro', 'category', 'subcategory', 'display_hashtags', 'pricing', 'created_at')
    search_fields = ('name', 'user__username', 'category__name', 'subcategory__name')
    list_filter = ('category', 'subcategory', 'pricing', 'created_at')

    def display_hashtags(self, obj):
        return ", ".join([hashtag.term for hashtag in obj.hashtag.all()])
    display_hashtags.short_description = 'Hashtags'




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


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'status','likes', 'created_on', 'updated_on')
    list_filter = ('status', 'created_on', 'updated_on')
    search_fields = ('title', 'content')



@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_tool', 'created_at')
    search_fields = ('user__username', 'user_tool__name')
    list_filter = ('created_at',)
    ordering = ('-created_at',)

    

