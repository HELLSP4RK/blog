from django.urls import path

from api.views import *

urlpatterns = [
    path('posts/', PostListView.as_view(), name='posts'),
]
