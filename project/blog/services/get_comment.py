from django.shortcuts import get_object_or_404

from blog.models import *


def get_comments_by_user(username):
    return Comment.objects.filter(author__username=username, status='visible').select_related('author', 'post')


def get_comment(pk):
    return get_object_or_404(Comment, id=pk)
