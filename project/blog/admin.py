from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from blog.models import *


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(MPTTModelAdmin):
    list_display = ('name', 'id', 'parent')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'author', 'published', 'status')
    list_display_links = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'content')


@admin.register(Comment)
class CommentAdmin(MPTTModelAdmin):
    list_display = ('content', 'author', 'parent', 'post', 'status')
    search_fields = ('author', 'content', 'post')


@admin.register(Subscription)
class SubscriptionsAdmin(admin.ModelAdmin):
    pass
