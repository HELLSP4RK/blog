from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UsernameField
from django.forms import *

from blog.models import User, Post


class LoginForm(AuthenticationForm):
    username = CharField(label='', widget=TextInput(attrs={'placeholder': 'Имя пользователя'}))
    password = CharField(label='', widget=PasswordInput(attrs={'placeholder': 'Пароль'}))


class RegisterForm(UserCreationForm):
    username = CharField(label='', widget=TextInput(attrs={'placeholder': 'Имя пользователя'}))
    email = EmailField(label='', widget=EmailInput(attrs={'placeholder': 'E-mail'}))
    password1 = CharField(label='', widget=PasswordInput(attrs={'placeholder': 'Пароль'}))
    password2 = CharField(label='', widget=PasswordInput(attrs={'placeholder': 'Повторите пароль'}))

    class Meta:
        model = User
        fields = ('username', 'email')
        field_classes = {'username': UsernameField,
                         'email': EmailField}


class UserEditForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'photo')


class AddPostForm(ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'category', 'photo', 'content', 'tags', 'status')
