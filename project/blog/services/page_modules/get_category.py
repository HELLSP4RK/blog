from django.db.models import Count

from blog.models import Category


def get_most_popular_cats():
    return Category.objects.annotate(posts_count=Count('posts')).order_by('-posts_count')[:10]


def get_breadcrumbs(category):
    return category.get_ancestors()
