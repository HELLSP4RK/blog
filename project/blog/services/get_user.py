from django.shortcuts import get_object_or_404

from blog.models import User


def get_user(username):
    return get_object_or_404(User, username=username)


def get_subscribers_by_category(cat):
    return cat.subscription.subscribers.all()
