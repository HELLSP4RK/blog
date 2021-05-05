from django.db.models import Count

from blog.models import Category


def get_most_popular_cats(how_much=10):
    return Category.objects.annotate(posts_count=Count('posts')).order_by('-posts_count')[:how_much]


def get_breadcrumbs(category):
    return category.get_ancestors()
