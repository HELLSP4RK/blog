from django.shortcuts import get_object_or_404

from blog.models import *


def get_root_categories():
    return Category.objects.filter(parent=None).annotate(posts_count=Count('posts'))


def get_child_categories(category):
    return category.get_children().annotate(posts_count=Count('posts'))


def get_category(slug):
    return get_object_or_404(Category, slug=slug)
