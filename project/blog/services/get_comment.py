from django.shortcuts import get_object_or_404

from blog.models import *
from blog.services.get_post import get_post


def get_comments_by_user(username):
    return Comment.objects.filter(author__username=username, status=Comment.Status.VISIBLE)\
        .select_related('author', 'post')


def get_comments_by_post(pk, slug):
    post = get_post(pk, slug)
    return Comment.objects.filter(post=post, status=Comment.Status.VISIBLE).select_related('author', 'post')


def get_comment(pk):
    return get_object_or_404(Comment, id=pk)
