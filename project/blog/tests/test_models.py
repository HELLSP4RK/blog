from django.test import TestCase

from blog.models import *


class PostModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        author = User.objects.create(username='usertest', password='secretpass')
        category = Category.objects.create(name='Категория')
        Post.objects.create(author=author,
                            title='Заголовок',
                            category=category,
                            content='Наполнение поста')

    def test_get_absolute_url(self):
        post = Post.objects.get(id=1)
        self.assertEquals(post.get_absolute_url(), '/post/1-zagolovok/')