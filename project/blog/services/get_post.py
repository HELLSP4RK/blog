from django.contrib.postgres.search import SearchRank, SearchQuery, SearchVector
from django.shortcuts import get_object_or_404

from blog.models import Post


def get_all_posts():
    return Post.objects.select_related('category', 'author')


def get_public_posts():
    return Post.publications.select_related('category', 'author')


def get_all_posts_by_user(username):
    return Post.objects.filter(author__username=username).select_related('category', 'author')


def get_public_posts_by_user(username):
    return Post.publications.filter(author__username=username).select_related('category', 'author')


def get_posts_by_category(slug):
    return Post.publications.filter(category__slug=slug).select_related('category', 'author')


def get_posts_by_tag(slug):
    return Post.publications.filter(tags__slug=slug).select_related('category', 'author')


def get_post(pk, slug):
    return get_object_or_404(Post, id=pk, slug=slug)


def get_posts_by_query(query):
    # search_similarity = TrigramSimilarity('title', query)
    # return Post.publications.annotate(similarity=search_similarity)\
    #     .filter(similarity__gt=0.3)\
    #     .order_by('-similarity')
    search_vector = SearchVector('title', weight='A') + SearchVector('content', weight='B')
    search_query = SearchQuery(query)
    search_rank = SearchRank(search_vector, search_query)
    return Post.publications.annotate(search=search_vector, rank=search_rank)\
        .filter(search=search_query)\
        .select_related('category', 'author')\
        .order_by('-rank')
