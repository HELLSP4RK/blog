from django.db.models import Count

from blog.models import Post


def get_main_posts():
    return Post.publications.select_related('category', 'author').filter(on_main_page=True)[:4]


def get_flash_posts(how_much=4):
    return Post.publications.filter(in_flash=True)[:how_much]


def get_most_popular_posts(how_much=5):
    return Post.publications.annotate(comments_num=Count('comments')
                                      ).select_related('category', 'author'
                                                       ).order_by('-comments_num', '-published')[:how_much]


def get_most_popular_posts_by_tag(tag: object, how_much=4):
    posts = Post.publications.filter(tags=tag)
    return posts.annotate(comments_count=Count('comments')
                          ).select_related('category', 'author').order_by('-comments_count')[:how_much]
