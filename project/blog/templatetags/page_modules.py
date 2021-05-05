from django import template

from blog.services.page_modules.get_post import *
from blog.services.page_modules.get_comment import *
from blog.services.page_modules.get_category import *
from blog.services.page_modules.get_tag import *


register = template.Library()


@register.inclusion_tag('blog/page_modules/main/main_posts.html')
def main_posts():
    posts = get_main_posts()
    if posts:
        return {
            'first_post': posts[0],
            'posts': posts[1:],
        }


@register.inclusion_tag('blog/page_modules/main/flash.html')
def flash():
    return {
        'posts': get_flash_posts(),
    }


@register.inclusion_tag('blog/page_modules/popular_posts.html')
def popular_posts():
    return {
        'posts': get_most_popular_posts(),
    }


@register.inclusion_tag('blog/page_modules/main/latest_posts.html')
def latest_posts(posts, how_much=5):
    return {
        'posts': posts[:how_much],
    }


@register.inclusion_tag('blog/page_modules/breadcrumbs.html')
def breadcrumbs(category):
    return {
        'breadcrumbs': get_breadcrumbs(category),
        'category': category,
    }


@register.inclusion_tag('blog/page_modules/main/tag_panel.html')
def tag_panel():
    tags = get_most_popular_tags()
    posts = list()
    for tag in tags:
        posts.append(get_most_popular_posts_by_tag(tag))
    values = list(zip(tags, posts))
    return {
        'values': values,
    }


@register.inclusion_tag('blog/page_modules/comments/comments.html')
def show_comments(post):
    return {'parents': get_comments_by_post(post),
            'post': post}


@register.inclusion_tag('blog/page_modules/comments/child_comments.html')
def child_comments(comment):
    return {'comments': comment.get_children()}


@register.inclusion_tag('blog/page_modules/main/categories.html')
def categories():
    return {
        'cats': get_most_popular_cats()
    }


@register.inclusion_tag('blog/page_modules/show_cats.html')
def show_cats(cat):
    return {
        'cat': cat,
        'child_cats_count': cat.get_children().count(),
        'posts_count': cat.posts_count,
    }


@register.inclusion_tag('blog/page_modules/social_auth.html')
def social_auth():
    pass
