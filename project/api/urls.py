from django.urls import path

from api.views import *

urlpatterns = [
    path('posts/all/', PostListView.as_view(), name='posts'),
    path('posts/user/<str:username>/', PostListByUserView.as_view(), name='posts_by_user'),
    path('posts/category/<slug:slug>/', PostListByCatView.as_view(), name='posts_by_category'),
    path('posts/tag/<slug:slug>/', PostListByTagView.as_view(), name='posts_by_tag'),
    path('post/<int:id>-<slug:slug>/', PostView.as_view(), name='post'),
    path('post/<int:id>-<slug:slug>/edit/', EditPostView.as_view(), name='edit_post'),
    path('post/<int:id>-<slug:slug>/remove/', RemovePostView.as_view(), name='remove_post'),

    path('post/add/', AddPostView.as_view(), name='add_post'),

    path('comments/user/<str:username>/', CommentListByUserView.as_view(), name='comments_by_user'),
    path('comments/post/<int:id>-<slug:slug>/', CommentListByPostView.as_view(), name='comments_by_post'),

    path('comment/add/', AddCommentView.as_view(), name='add_comment'),

    path('user/<str:username>/', UserView.as_view(), name='user'),

    path('categories/root/', RootCatListView.as_view(), name='categories'),
    path('categories/category/<slug:slug>/', CatListByCatView.as_view(), name='categories_by_category'),
]
