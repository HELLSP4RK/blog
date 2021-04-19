from django.db.models import Count

from blog.models import Post


def get_main_posts():
    return Post.publications.select_related('category', 'author').filter(on_main_page=True)[:4]


def get_flash_posts():
    return Post.publications.filter(in_flash=True)[:4]


def get_most_popular_posts():
    return Post.publications.annotate(comments_num=Count('comments')
                                      ).select_related('category', 'author').order_by('-comments_num', '-published')[:4]


def get_most_popular_posts_by_tag(tag: object):
    posts = Post.publications.filter(tags=tag)
    return posts.annotate(comments_count=Count('comments')
                          ).select_related('category', 'author').order_by('-comments_count')[:4]