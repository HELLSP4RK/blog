from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetConfirmView, \
    PasswordChangeView
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, FormView, CreateView, UpdateView
from django.views.generic.edit import DeleteView

from blog.forms import *


from blog.services.get_post import *
from blog.services.get_comment import *
from blog.services.get_category import *
from blog.services.get_tag import *
from blog.services.get_user import *

from blog.services.add_object import *
from blog.services.update_object import *

from blog.services.get_count import *


from blog.utils import ContextMixin
from project import settings


class LoginUserView(ContextMixin, LoginView):
    form_class = LoginForm
    template_name = 'blog/login.html'

    def get_context_data(self, *args, **kwargs):
        context = {
            'title': 'Авторизация',
        }
        return self.get_user_context(**context)


class LogoutUserView(LogoutView):
    next_page = 'blog:login'

    def post(self, request, *args, **kwargs):
        return logout(request)


class RegisterUserView(ContextMixin, FormView):
    form_class = RegisterForm
    template_name = 'blog/register.html'
    success_url = reverse_lazy('blog:main')

    def get_context_data(self, *args, **kwargs):
        context = {
            'title': 'Регистрация',
        }
        return self.get_user_context(**context)

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return super(RegisterUserView, self).form_valid(form)


class AddPostView(LoginRequiredMixin, ContextMixin, CreateView):
    model = Post
    success_url = reverse_lazy('blog:main')
    form_class = AddPostForm
    template_name = 'blog/add_edit_post.html'

    def get_context_data(self, *args, **kwargs):
        context = {
            'title': 'Создание поста',
        }
        return self.get_user_context(**context)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return super(AddPostView, self).form_valid(form)


class EditPostView(LoginRequiredMixin, ContextMixin, UpdateView):
    form_class = AddPostForm
    template_name = 'blog/add_edit_post.html'
    pk_url_kwarg = 'id'

    def get_success_url(self):
        return reverse('blog:posts_by_user', kwargs={'username': self.request.user.username})

    def get_object(self, **kwargs):
        pk = self.kwargs[self.pk_url_kwarg]
        slug = self.kwargs[self.slug_url_kwarg]
        return get_post(pk, slug)

    def get_context_data(self, **kwargs):
        context = {
            'title': f'Редактирование поста {self.object.title}',
        }
        return self.get_user_context(**context)


class RemovePostView(LoginRequiredMixin, ContextMixin, DeleteView):
    context_object_name = 'post'
    template_name = 'blog/remove.html'
    pk_url_kwarg = 'id'

    def get_context_data(self, *args, **kwargs):
        context = {
            'title': 'Удаление поста',
            'username': self.request.user.username,
        }
        return self.get_user_context(**context)

    def delete(self, request, *args, **kwargs):
        post = self.get_object()
        if self.request.user == post.author:
            post.delete()
            return self.get_success_url()
        raise PermissionDenied()

    def get_success_url(self):
        return redirect('blog:posts_by_user', username=self.request.user.username)

    def get_object(self, **kwargs):
        pk = self.kwargs[self.pk_url_kwarg]
        slug = self.kwargs[self.slug_url_kwarg]
        return get_post(pk, slug)


class UserView(ContextMixin, DetailView):
    context_object_name = 'user'
    template_name = 'blog/user.html'

    def get_context_data(self, *args, **kwargs):
        """Получаем username из уже выполненного запроса в методе get_object и передаем его в title"""
        context = {
            'title': f"Пользователь {self.object.username}",
            'posts_count': get_posts_count_by_user(user=self.object),
            'comments_count': get_comments_count_by_user(user=self.object),
            'photo_height': 350,
            'photo_width': 250,
        }
        return self.get_user_context(**context)

    def get_object(self, **kwargs):
        return get_user(username=self.kwargs['username'])


class ForgotPasswordView(ContextMixin, PasswordResetView):
    template_name = 'blog/password.html'
    email_template_name = 'blog/emails/password_reset_email.html'
    form_class = PasswordResetForm
    title = 'Изменение пароля'
    success_url = reverse_lazy('blog:main')

    def get_context_data(self, **kwargs):
        context = {
            'button': 'Отправить',
        }
        return self.get_user_context(**context)
    
    def form_valid(self, form):
        return super(ForgotPasswordView, self).form_valid(form)


class ChangeForgottenPasswordView(ContextMixin, PasswordResetConfirmView):
    template_name = 'blog/password.html'
    form_class = SetPasswordForm
    title = 'Изменение пароля'
    success_url = reverse_lazy('blog:login')

    def get_context_data(self, **kwargs):
        context = {
            'button': 'Изменить',
        }
        return self.get_user_context(**context)

    def form_valid(self, form):
        return super(ChangeForgottenPasswordView, self).form_valid(form)


class ChangePasswordView(LoginRequiredMixin, ContextMixin, PasswordChangeView):
    template_name = 'blog/password.html'
    title = 'Изменение пароля'
    success_url = reverse_lazy('blog:settings')

    def get_context_data(self, **kwargs):
        context = {
            'button': 'Изменить',
        }
        return self.get_user_context(**context)


class UserSettingsView(LoginRequiredMixin, ContextMixin, UpdateView):
    form_class = UserEditForm
    template_name = 'blog/user_settings.html'
    success_url = reverse_lazy('blog:settings')

    def get_object(self, queryset=None):
        return get_user(self.request.user.username)

    def get_context_data(self, *args, **kwargs):
        return self.get_user_context(title='Настройки учетной записи')


class AuthUserView(LoginRequiredMixin, ContextMixin, DetailView):
    context_object_name = 'user'
    template_name = 'blog/user.html'

    def get_context_data(self, *args, **kwargs):
        """Получаем username из уже выполненного запроса в методе get_object и передаем его в title"""
        context = {
            'title': f"Пользователь {self.object.username}",
            'posts_count': get_posts_count_by_user(user=self.object),
            'comments_count': get_comments_count_by_user(user=self.object),
            'photo_height': 350,
            'photo_width': 250,
        }
        return self.get_user_context(**context)

    def get_object(self, **kwargs):
        return self.request.user


class MainPageView(ContextMixin, ListView):
    context_object_name = 'posts'
    template_name = 'blog/index.html'

    def get_context_data(self, *args, **kwargs):
        context = {
            'title': 'Блог',
        }
        return self.get_user_context(**context)

    def get_queryset(self):
        return get_public_posts()


class PostView(ContextMixin, DetailView):
    context_object_name = 'post'
    template_name = 'blog/post.html'
    pk_url_kwarg = 'id'

    def get_context_data(self, *args, **kwargs):
        context = {
            'title': f'{self.object}',
            'comments_count': get_comments_count_by_post(self.object),
        }
        return self.get_user_context(**context)

    def get_object(self, **kwargs):
        pk = self.kwargs[self.pk_url_kwarg]
        slug = self.kwargs[self.slug_url_kwarg]
        post = get_post(pk, slug)
        if post.status == Post.Status.DRAFT and post.author != self.request.user:
            raise PermissionDenied
        return post


@login_required
def comment_adding(request):
    author = request.user
    post_id = request.POST.get('post_id')
    post_slug = request.POST.get('post_slug')
    content = request.POST.get('comment')
    parent_id = request.POST.get('parent_id')
    add_comment(author, post_id, post_slug, content, parent_id)
    return redirect('blog:post', id=post_id, slug=post_slug)


@login_required
def subscribe_or_unsubscribe(request):
    category_slug = request.GET.get('category_slug')
    category = get_category(category_slug)
    subscribe_or_unsubscribe_user(category, request.user)
    return redirect('blog:category', slug=category_slug)


class PostListView(ContextMixin, ListView):
    context_object_name = 'posts'
    paginate_by = settings.PAGINATE_BY
    template_name = 'blog/posts.html'

    def get_context_data(self, *args, **kwargs):
        context = {
            'title': 'Все посты',
            'count': get_queryset_count(self.object_list)
        }
        return self.get_user_context(**context)

    def get_queryset(self):
        return get_public_posts()


class CatListView(ContextMixin, ListView):
    context_object_name = 'cats'
    paginate_by = settings.PAGINATE_BY
    template_name = 'blog/categories.html'

    def get_context_data(self, *args, **kwargs):
        context = {
            'title': 'Родительские категории',
            'cats_count': get_queryset_count(self.object_list)
        }
        return self.get_user_context(**context)

    def get_queryset(self):
        return get_root_categories()


class TagListView(ContextMixin, ListView):
    context_object_name = 'tags'
    template_name = 'blog/tags.html'

    def get_context_data(self, *args, **kwargs):
        context = {
            'title': 'Теги',
            'count': get_queryset_count(self.object_list)
        }
        return self.get_user_context(**context)

    def get_queryset(self):
        return get_all_tags()


class PostListByCatView(ContextMixin, ListView):
    context_object_name = 'posts'
    paginate_by = settings.PAGINATE_BY
    template_name = 'blog/category.html'

    def get_context_data(self, *args, **kwargs):
        category = get_category(slug=self.kwargs['slug'])
        child_cats = get_categorys_children(category)
        title = f'Категория "{category}"'
        posts_count = get_queryset_count(self.object_list)
        cats_count = get_queryset_count(child_cats)
        subscribers = get_subscribers_by_category(category)
        context = {
            'title': title,
            'category': category,
            'child_cats': child_cats,
            'posts_count': posts_count,
            'cats_count': cats_count,
            'subscribers': subscribers,
        }
        return self.get_user_context(**context)

    def get_queryset(self):
        return get_posts_by_category(slug=self.kwargs['slug'])


class PostListByTagView(ContextMixin, ListView):
    context_object_name = 'posts'
    template_name = 'blog/posts.html'

    def get_context_data(self, *args, **kwargs):
        tag = get_tag(slug=self.kwargs['slug'])
        context = {
            'title': f'Посты по тегу "{tag}"',
            'count': get_queryset_count(self.object_list),
        }
        return self.get_user_context(**context)

    def get_queryset(self):
        return get_posts_by_tag(slug=self.kwargs['slug'])


class PostListByUserView(ContextMixin, ListView):
    context_object_name = 'posts'
    template_name = 'blog/user_posts.html'
    paginate_by = settings.PAGINATE_BY

    def __own_page(self):
        return self.request.user.username == self.kwargs['username']

    def get_context_data(self, *args, **kwargs):
        context = {
            'title': f"Посты пользователя {get_user(username=self.kwargs['username'])}",
            'count': get_queryset_count(self.object_list),
            'own_page': self.__own_page(),
        }
        return self.get_user_context(**context)

    def get_queryset(self):
        """Если пользователь просматривает свои посты, то показать все. Если чужие, то только опубликованные"""
        username = self.kwargs['username']
        if self.__own_page():
            return get_all_posts_by_user(username)
        return get_public_posts_by_user(username)


class CommentsListByUserView(ContextMixin, ListView):
    context_object_name = 'comments'
    template_name = 'blog/user_comments.html'
    paginate_by = settings.PAGINATE_BY

    def get_context_data(self, *args, **kwargs):
        context = {
            'title': f"Комментарии пользователя {self.kwargs['username']}",
            'count': get_queryset_count(self.object_list),
        }
        return self.get_user_context(**context)

    def get_queryset(self):
        return get_comments_by_user(self.kwargs['username'])


class SearchView(ContextMixin, ListView):
    context_object_name = 'posts'
    paginate_by = settings.PAGINATE_BY
    template_name = 'blog/search/index.html'
    
    def get_context_data(self, *args, **kwargs):
        query = self.request.GET.get('query')
        context = {
            'title': f'Поиск: {query}',
            'count': get_queryset_count(self.object_list),
            'last_query': query,
        }
        return self.get_user_context(**context)
    
    def get_queryset(self):
        query = self.request.GET.get('query')
        return get_posts_by_query(query)


def contact(request):
    return render(request, 'blog/contact.html')
