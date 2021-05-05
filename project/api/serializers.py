from rest_framework.fields import *
from rest_framework.serializers import ModelSerializer

from blog.models import Post
from blog.services.get_user import get_user


class PostSerializer(ModelSerializer):
    id = ReadOnlyField()
    author = SerializerMethodField()
    category = SerializerMethodField()

    def get_author(self, obj):
        return obj.author.username

    def get_category(self, obj):
        return obj.category.name

    class Meta:
        model = Post
        exclude = ('on_main_page', 'in_flash', 'notificated')
