from django.db.models import Count
from django.shortcuts import get_object_or_404
from taggit.models import Tag


def get_all_tags():
    return Tag.objects.annotate(posts_count=Count('taggit_taggeditem_items')).order_by('-posts_count')


def get_tag(slug):
    return get_object_or_404(Tag, slug=slug)
