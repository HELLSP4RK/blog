from django.urls import path

from blog.views import *

urlpatterns = [
    path('', MainPageView.as_view(), name='main'),

    # Вход, выход и регистрация
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
    path('register/', RegisterUserView.as_view(), name='register'),

    path('add_post/', AddPostView.as_view(), name='add_post'),
    path('post/<int:id>-<slug:slug>/', PostView.as_view(), name='post'),
    path('post/<int:id>-<slug:slug>/edit/', EditPostView.as_view(), name='edit_post'),
    path('post/<int:id>-<slug:slug>/remove/', RemovePostView.as_view(), name='remove_post'),
    path('posts/', PostListView.as_view(), name='posts'),
    path('categories/', CatListView.as_view(), name='categories'),
    path('tags/', TagListView.as_view(), name='tags'),
    path('search/', SearchView.as_view(), name='search'),
    path('category/<slug:slug>/', PostListByCatView.as_view(), name='category'),
    path('tag/<slug:slug>/', PostListByTagView.as_view(), name='tag'),
    path('accounts/profile/', AuthUserView.as_view(), name='auth_user'),
    path('accounts/<username>/', UserView.as_view(), name='user'),
    path('accounts/<username>/posts/', PostListByUserView.as_view(), name='posts_by_user'),
    path('accounts/<username>/comments/', CommentsListByUserView.as_view(), name='comments_by_user'),
    path('settings/', UserSettingsView.as_view(), name='settings'),

    # Обработчики восстановления пароля
    path('forgot_password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('reset/<uidb64>/<token>/', ChangeForgottenPasswordView.as_view(), name='change_forgotten_password'),
    path('change_password/', ChangePasswordView.as_view(), name='change_password'),

    path('add_comment/', comment_adding, name='add_comment'),
    path('subscribe_or_unsubscribe/', subscribe_or_unsubscribe, name='subscribe_or_unsubscribe'),

    path('contact/', contact, name='contact'),
]