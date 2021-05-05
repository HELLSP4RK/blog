from django.shortcuts import render
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import *
from blog.services.get_post import get_public_posts, get_post


class PostListView(ListAPIView):
    queryset = get_public_posts()
    serializer_class = PostSerializer
