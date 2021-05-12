from rest_framework.fields import *
from rest_framework.serializers import ModelSerializer
from taggit_serializer.serializers import TagListSerializerField, TaggitSerializer

from blog.models import Post, Comment, User, Category
from blog.services.get_category import get_child_categories
from blog.services.get_count import get_posts_count_by_user, get_comments_count_by_user, get_comments_count_by_post, \
    get_queryset_count


class PostSerializer(ModelSerializer):
    id = ReadOnlyField()
    author = SerializerMethodField()
    category = SerializerMethodField()
    comments = SerializerMethodField()

    def get_author(self, obj):
        return obj.author.username

    def get_category(self, obj):
        return obj.category.name

    def get_comments(self, obj):
        return get_comments_count_by_post(obj)

    class Meta:
        model = Post
        exclude = ('on_main_page', 'in_flash', 'notificated')


class CommentSerializer(ModelSerializer):
    id = ReadOnlyField()
    author = SerializerMethodField()
    post = SerializerMethodField()

    def get_author(self, obj):
        return obj.author.username

    def get_post(self, obj):
        return obj.post.title

    class Meta:
        model = Comment
        fields = ('id', 'author', 'post', 'content', 'created', 'parent')


class CategorySerializer(ModelSerializer):
    posts = SerializerMethodField()
    categories = SerializerMethodField()

    def get_posts(self, obj):
        return obj.posts_count

    def get_categories(self, obj):
        child_cats = get_child_categories(obj)
        return get_queryset_count(child_cats)

    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', 'posts', 'categories', 'parent')


class UserSerializer(ModelSerializer):
    posts = SerializerMethodField()
    comments = SerializerMethodField()

    def get_posts(self, obj):
        return get_posts_count_by_user(user=obj, auth_user=self.context['request'].user)

    def get_comments(self, obj):
        return get_comments_count_by_user(user=obj)

    class Meta:
        model = User
        exclude = ('password', 'first_name', 'last_name', 'groups', 'user_permissions')


class AddPostSerializer(TaggitSerializer, ModelSerializer):
    author = HiddenField(default=CurrentUserDefault())
    tags = TagListSerializerField()

    class Meta:
        model = Post
        fields = ('author', 'title', 'category', 'tags', 'photo', 'content', 'status')


class AddCommentSerializer(ModelSerializer):
    author = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Comment
        fields = ('id', 'author', 'post', 'content', 'created', 'parent')
